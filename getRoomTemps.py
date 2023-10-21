from threading import Thread
from pythonosc import udp_client
from time import sleep
from requests import get

# Dispatcher lets you map functions to events: dispatcher.map("/example/address", handle_message)
c = udp_client.SimpleUDPClient("127.0.0.1", 9000)

def getData():
    d = get("http://192.168.254.169/").json()
    return d["temperature"], d["humidity"], d["co2"]

def sendChat(message):
    thread = Thread(target=c.send_message, args=("/chatbox/input", [message, True]))
    thread.start()

def main():
    while True:
        t, h, co2 = getData()
        sendChat(f"Room stats: {round(t, 1)}F, CO2: {co2} ppm")
        sleep(5)
        #/{round((t-32)*(5/9), 2)}C

if __name__ == "__main__":
    main()