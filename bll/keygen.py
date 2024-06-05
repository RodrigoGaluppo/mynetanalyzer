from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate RSA key pair for the server
private_key = rsa.generate_private_key(
    public_exponent=65537, # common prime number used
    key_size=2048, 
    backend=default_backend()
)

# Serialize private key to PEM format
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Serialize public key to PEM format
public_key_pem = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save keys to files or store them securely
with open('./producer/server_private_key.pem', 'wb') as f:
    f.write(private_key_pem)

with open('../host/server_public_key.pem', 'wb') as f:
    f.write(public_key_pem)
