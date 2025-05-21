from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


# Generate RSA key pair
def generate_keys(key_size=4096):
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


if __name__ == "__main__":
    import time

    test_message = (
        "Hello, this is a performance test for RSA encryption and decryption!"
    )

    # Call your own functions for testing
    private_key, public_key = generate_keys()

    start_enc = time.time()
    encrypted = encrypt_message(test_message, public_key)
    end_enc = time.time()
    print(f"Encryption time: {end_enc - start_enc:.6f} seconds")

    start_dec = time.time()
    decrypted = decrypt_message(encrypted, private_key)
    end_dec = time.time()
    print(f"Decryption time: {end_dec - start_dec:.6f} seconds")
    print(f"Decrypted message: {decrypted}")
