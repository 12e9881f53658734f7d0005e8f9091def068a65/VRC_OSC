from threading import Thread
from pythonosc import udp_client
from time import sleep
from win32gui import EnumWindows, GetWindowText
from win32process import GetWindowThreadProcessId
from psutil import process_iter

# Biggest issue - uses a decent amount of cpu and ram when it updates 
updateSpeed = 5 # In seconds
match = " - "

c = udp_client.SimpleUDPClient("127.0.0.1", 9000)

def getPIDSFromProcessName(processName):
    pids = []

    for p in process_iter():
        if processName in p.name():
            pids.append(p.pid)
    
    return pids

def getHwndsOfPID(pid):
    def c(hwnd, hwnds):
        if GetWindowThreadProcessId(hwnd)[1] == pid:
            hwnds.append(hwnd)

    hwnds = []
    EnumWindows(c, hwnds)

    return hwnds 

def getSpotifyCurrentlyPlaying():
    pids = getPIDSFromProcessName("Spotify.exe")

    for pid in pids:
        hwnds = getHwndsOfPID(pid)
        for hwnd in hwnds:
            title = GetWindowText(hwnd)
            if match in title:
                return title

def sendChat(message):
    thread = Thread(target=c.send_message, args=("/chatbox/input", [message, True]))
    thread.start()

def main():
    lastSong = ""
    while True:
        spotifySong = getSpotifyCurrentlyPlaying()
        if spotifySong == None:
            spotifySong = "Music stopped"
        if spotifySong and spotifySong != lastSong:
            lastSong = spotifySong
            sendChat(spotifySong)
        sleep(updateSpeed)

if __name__ == "__main__":
    main()