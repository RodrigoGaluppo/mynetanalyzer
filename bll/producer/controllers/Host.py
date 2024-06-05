from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Global import sessionMaker
from models.TimeSeriesPacket import TimeSeriesPacket
from datetime import datetime

pr_key = RSA.import_key(open('server_private_key.pem', 'r').read())

#Instantiating PKCS1_OAEP object with the private key for decryption
decrypt = PKCS1_OAEP.new(key=pr_key)

def parse_packet_summary(summary: bytes):
    try:
        
        summary_str = summary.decode('utf-8').strip("b'")
        
        if(">" in summary_str):
            main_src,main_dest = summary_str.split(">")
            
            items_list = main_src.replace("/","").split(" ")
            items_list = [item for item in items_list if item != str("")]
            
            src = items_list[-1]
            protocol = items_list[-2]
            dst = main_dest.split(" ")[1]
            size, timing = main_dest.split("|")[1].split(",")
            
            src_port = ""
            dst_port= ""
            
            if(":" in src):
                src_port = src.split(":")[-1]
                src = src.split(":")[0]
            else:
                src_port = ""
                
                
            if(":" in dst):
                dst_port = dst.split(":")[-1]
                dst = dst.split(":")[0]
            else:
                dst_port = ""
               
            
            return {
                "src":src,
                "dst":dst,
                "protocol":protocol,
                "size":size,
                "timing":timing,
                "src_port":src_port,
                "dst_port":dst_port
            }
            
            
        elif("says" in summary_str): # ARP
            
            main_src,main_dest = summary_str.split("says")
            
            items_list = main_src.replace("/","").split(" ")
            items_list = [item for item in items_list if item != str("")]
            
            src = items_list[-1]
            protocol = items_list[-4]
            dst = main_dest.split(" ")[1]
            size, timing = main_dest.split("|")[1].split(",")
            
            src_port = ""
            dst_port= ""
            
            
            return {
                "src":src,
                "dst":dst,
                "protocol":protocol,
                "size":size,
                "timing":timing,
                "src_port":src_port,
                "dst_port":dst_port
            }
                
        else:
            return None
         
    except Exception as e:
        print(f"Error parsing summary: {e}")
        return None
    
async def host(websocket):
    async for message in websocket:
        
        session = sessionMaker()
        
        decrypted_message = decrypt.decrypt(message)
        
        parsed_packet = parse_packet_summary(decrypted_message)
        
        # If packet is successfully normalized
        if(parsed_packet != None):
              session.add(TimeSeriesPacket(
                src=parsed_packet.get("src"),   
                dst=parsed_packet.get("dst"),
                timing=parsed_packet.get("timing"),
                protocol=parsed_packet.get("protocol"),
                size=parsed_packet.get("size"),
                src_port=parsed_packet.get("src_port"),
                dst_port=parsed_packet.get("dst_port"),
                ip_address=websocket.remote_address[0].replace(")","").replace("(","")
        ))
       
        
        # troubleshoot
        print("----- packet ----")
        print(decrypted_message)
        print("-------" + str(websocket.remote_address) + "---------")
              
        session.commit()

        session.close()
        
        