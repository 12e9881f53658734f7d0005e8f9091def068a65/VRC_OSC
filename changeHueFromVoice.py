import threading
from pythonosc import osc_server, dispatcher, udp_client
from random import random

ip = "127.0.0.1"
AP = "/avatar/parameters"
c = udp_client.SimpleUDPClient(ip, 9000)

def start():
    s = osc_server.ThreadingOSCUDPServer((ip, 9001), dispatcher)
    t = threading.Thread(target=s.serve_forever)
    t.daemon = True
    t.start()

def send(address, data):
    thread = threading.Thread(target=c.send_message, args=(address, data))
    thread.start()

def catThing(address, value):
    send(f"{AP}/HueShiftRimlight", [value])
    # send(f"{AP}/HueShiftRimlight", [0.45152056217193604])


def main():
    dispatcher.map(f"{AP}/Voice", catThing)
    start()

if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()
    main()

    input("")
