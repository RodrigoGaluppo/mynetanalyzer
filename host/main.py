from scapy.all import *
import psutil

class NetworkPacket:
    def __init__(self, packet):
        self.ip_src = packet[IP].src if "IP" in packet else None
        self.ip_dst = packet[IP].dst if "IP" in packet else None
        self.ip_version = packet[IP].version if "IP" in packet else None
        self.src = packet.src if "Ether" in packet else None
        self.dst = packet.dst if "Ether" in packet else None
        self.src_port = packet.sport 
        self.dst_port = packet.dport 
        self.protocol = packet.proto 
        self.tcpudp_flags = packet.flags 
        self.payload = packet.payload if packet.payload else None
        #self.raw_payload = str(self.payload.original) if self.payload else None
        self.packet_length = len(packet)
        self.timestamp = packet.time               
        self.process = self.get_process(packet)

    def get_process(self, packet):
        try:
            # Extract source and destination IP addresses and ports
            src = packet[IP].src if IP in packet else None
            src_port = packet[TCP].sport if TCP in packet else None
          
            # match the process based on port and ip 
            connections = psutil.net_connections()
            for conn in connections:
                if (
                    conn.laddr.ip == src
                    and conn.laddr.port == src_port
                ):
                    return psutil.Process(conn.pid).name()
                
        except Exception as e:
            print(f"Error occurred while retrieving process: {e}")
        return None
    
    def __str__(self):
        return f"------ " \
            f"Network Packet: \nsrc_ethernet : {self.src} \ndst_ethernet: {self.dst}, \n" \
            f"src_ip : {self.ip_src} \ndst_ip: {self.ip_dst} \nversion:{self.ip_version}\n" \
            f"src_port: {self.src_port}, dst_port: {self.dst_port}, \n" \
            f"proto: {self.protocol}, TCPudp_flags: {self.tcpudp_flags}, \n" \
            f"payload: {self.payload} \nlenght: {self.packet_length}, \n" \
            f"timestamp: {self.timestamp} \n" \
            f"process: {self.process}\n" \
            f"------ \n" 

# Dictionary to store fragmented packets
fragmented_packets = {}

def packet_callback(packet):
    
    try:
        network_packet = NetworkPacket(packet)
        print(network_packet)
    except Exception as e:
        print(e)


# Sniff packets on the default network interface
sniff(prn=packet_callback, store=0)
