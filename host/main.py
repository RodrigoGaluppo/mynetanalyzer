from websockets.sync.client import connect
from scapy.all import *
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import configparser


config = configparser.ConfigParser()
config.read('default.conf')

server_ip = config.get('DEFAULT', 'server_ip')
server_port = config.get('DEFAULT', 'server_port')
public_key_path = config.get('DEFAULT', 'public_key_path')


pu_key = RSA.import_key(open(public_key_path, 'r').read())

def packet_callback(packet, ws):
    try:
        network_packet = packet.summary() + f" | {len(packet)}, {packet.time}"
        cipher = PKCS1_OAEP.new(key=pu_key)
        cipher_text = cipher.encrypt(str(network_packet).encode("utf-8"))
        ws.send(cipher_text)
        time.sleep(0.01)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        print("host sniffing alive")
        with connect(f"ws://{server_ip}:{server_port}") as websocket:
            sniff(prn=lambda packet: packet_callback(packet, websocket), store=0,
                  filter=f"not (src host {server_ip} or dst host {server_ip})")
    except Exception as err:
        time.sleep(3)
        print(err)
