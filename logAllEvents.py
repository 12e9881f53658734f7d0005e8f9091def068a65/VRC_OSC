import threading
from pythonosc import osc_server, dispatcher, udp_client

h = ["ToeTwist", "Spine", ""]

def start_server(ip="127.0.0.1", port=9001):
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

def receive_message(address, *args):
    if "ToeTwist" in address or "Spine" in address or "ToeCurl"  in address:
        pass
    else:
        print(f"Get  {address}:{args[0]}")

def main():
    dispatcher.map("/.*", receive_message)
    start_server()

if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()
    main()
    input("quit?\n")