import socket
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization

# Replace with your private key in PEM format (generated from your public key)
server_private_key = """MIIEvQIBAAKCAQEA"""

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def decrypt_data(encrypted_data, server_private_key):
  # Load private key from PEM format
  private_key = load_pem_private_key(server_private_key)
  
  
  
  # Extract IV, ciphertext, authentication tag, and data hash from received data
  iv = encrypted_data[:16]
  ciphertext = encrypted_data[16:-32]
  auth_tag = encrypted_data[-32:]
  data_hash = encrypted_data[-64:]
  
  
  # Decrypt the data using AES-GCM with the private key
  decryptor = private_key.decrypt(
      ciphertext,
      mode=modes.GCM(iv),
      encryption_algorithm=algorithms.AES(private_key.public_key()),
      authenticator=auth_tag
  )
  # Verify data integrity using the hash
  h = hashes.Hash(hashes.SHA256(), backend=default_backend())
  h.update(decryptor)
  if h.finalize() != data_hash:
      raise ValueError("Data integrity verification failed")
  return decryptor

def load_pem_private_key(pem_encoded_key):
  return serialization.load_pem_private_key(
      pem_encoded_key.encode('utf-8'),
      password=None,
      backend=default_backend()
  )

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Server listening for connections on {}:{}'.format(HOST, PORT))
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            # Receive encrypted data from the client
            encoded_data = conn.recv(1024).decode('utf-8')
            if not encoded_data:
                break
            # Decrypt the received data
            try:
                data = decrypt_data(base64.b64decode(encoded_data), server_private_key)
                print('Received data:', data.decode('utf-8'))
            except ValueError as e:
                print("Error:", e)
