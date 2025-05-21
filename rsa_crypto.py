from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


# Generate RSA key pair
def generate_keys(key_size=2048):
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


# Encrypt message with public key
def encrypt_message(message, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted = cipher.encrypt(message.encode())
    return encrypted  # Return raw bytes


# Decrypt message with private key
def decrypt_message(encrypted_message, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    decrypted = cipher.decrypt(encrypted_message)
    return decrypted.decode()
