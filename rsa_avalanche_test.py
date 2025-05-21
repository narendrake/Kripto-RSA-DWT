from rsa_crypto import generate_keys, encrypt_message
import binascii


def bit_diff_count(bytes1, bytes2):
    # Count differing bits between two byte strings
    diff = 0
    for b1, b2 in zip(bytes1, bytes2):
        xor = b1 ^ b2
        diff += bin(xor).count("1")
    return diff


def flip_bit_in_string(s, byte_index=0, bit_index=0):
    # Flip a bit at (byte_index, bit_index) in the UTF-8 encoded string
    b = bytearray(s.encode())
    b[byte_index] ^= 1 << bit_index
    return b.decode(errors="replace")


if __name__ == "__main__":
    msg = "AvalancheTestRSA"
    print(f"Original message: {msg}")

    # Generate keys
    private_key, public_key = generate_keys()

    # Encrypt original message
    encrypted1 = encrypt_message(msg, public_key)

    # Flip the first bit of the first byte in the message
    msg_flipped = flip_bit_in_string(msg, byte_index=0, bit_index=0)
    print(f"Flipped message:  {msg_flipped}")

    # Encrypt flipped message
    encrypted2 = encrypt_message(msg_flipped, public_key)

    # Compare ciphertexts
    diff_bits = bit_diff_count(encrypted1, encrypted2)
    total_bits = len(encrypted1) * 8
    print(f"Ciphertext 1: {binascii.hexlify(encrypted1).decode()}")
    print(f"Ciphertext 2: {binascii.hexlify(encrypted2).decode()}")
    print(
        f"Different bits: {diff_bits} / {total_bits} ({100*diff_bits/total_bits:.2f}%)"
    )
