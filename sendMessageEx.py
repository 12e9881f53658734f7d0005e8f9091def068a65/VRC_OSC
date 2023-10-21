import threading
from pythonosc import osc_server, dispatcher, udp_client
from time import sleep
import requests

# Dispatcher lets you map functions to events: dispatcher.map("/example/address", handle_message)
c = udp_client.SimpleUDPClient("127.0.0.1", 9000)

def sendChat(message):
    thread = threading.Thread(target=c.send_message, args=("/chatbox/input", [message, True, False]))
    thread.start()

def main():
        sendChat("--\u000A")

if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()
    main()
