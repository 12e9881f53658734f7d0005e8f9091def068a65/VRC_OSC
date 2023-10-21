from threading import Thread
from pythonosc import udp_client
from time import sleep
from win32gui import EnumWindows, GetWindowText
from win32process import GetWindowThreadProcessId
from psutil import process_iter
from requests import get

# Biggest issue - uses a decent amount of cpu and ram when it updates 
updateSpeed = 10 # In seconds
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

def getData():
    d = get("http://192.168.254.169/").json()
    return d["temperature"], d["humidity"], d["co2"]

def sendChat(message):
    thread = Thread(target=c.send_message, args=("/chatbox/input", [message, True]))
    thread.start()

def main():
    lastSong = ""
    lastSentTemp = False
    
    while True:
        message = ""
        """
        if lastSentTemp:
            currentSong = getSpotifyCurrentlyPlaying()
            if currentSong != lastSong:
                message = currentSong
                lastSong = currentSong
                sendChat(message)
            lastSentTemp = False
        else:
            t, h = getData()
            message = f"Room Temp: {round(t, 1)}F/{round((t-32)*(5/9), 2)}C"
            lastSentTemp = True
            sendChat(message) # make only one sendchat cos one var
        """
        currentSong = getSpotifyCurrentlyPlaying()
        if currentSong == None:
            currentSong = "No song playing"
        t, h, co2 = getData()
        # message = f"""Room Temp: {round(t, 1)}F/{round((t-32)*(5/9), 2)}C, CO2: {co2} ppm, Song: {currentSong}"""
        message = f"Tmp: {round(t, 1)}F \u2028CO2: {co2} ppm\u2028 Song: {currentSong}"
        sendChat(message)
        
        sleep(updateSpeed)


if __name__ == "__main__":
    main()