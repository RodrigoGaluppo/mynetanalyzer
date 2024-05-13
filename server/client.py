import websocket
from scapy.all import *

def packet_callback(packet):
    if not (packet[TCP].dport == 8080):
        payload = str(packet.payload)
        print(payload)
        ws.send(payload)

if __name__ == "__main__":
    ws = websocket.WebSocket()

    ws.connect("wss://localhost:8080/websocket")
    print("here")
    sniff(prn=packet_callback, store=0)
