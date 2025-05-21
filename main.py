from rsa_crypto import generate_keys, encrypt_message, decrypt_message
from audio_utils import read_wav, write_wav
import numpy as np
import dwt_stegano


def repeat_bits(bits, n=5):
    return "".join(bit * n for bit in bits)


def majority_vote(bits, n=5):
    result = ""
    for i in range(0, len(bits), n):
        chunk = bits[i : i + n]
        if len(chunk) == n:
            result += "1" if chunk.count("1") > chunk.count("0") else "0"
    return result


# Step 1: Generate RSA keys
def save_keys():
    private_key, public_key = generate_keys()
    with open("keys/private.pem", "wb") as f:
        f.write(private_key)
    with open("keys/public.pem", "wb") as f:
        f.write(public_key)
    print("Keys saved as private.pem and public.pem")


def encrypt_and_embed(text, input_audio, output_audio, n_repetition=5):
    # Encrypt text with RSA
    with open("keys/public.pem", "rb") as f:
        public_key = f.read()
    encrypted = encrypt_message(text, public_key)
    enc_len = len(encrypted)
    # Convert encrypted bytes to bits
    bits = "".join(f"{byte:08b}" for byte in encrypted)
    # Prepare sync marker and length (in bytes)
    sync_marker = "1010101010101010"
    msg_length = format(enc_len, "016b")
    data_to_embed = sync_marker + msg_length + bits
    repeated_bits = repeat_bits(data_to_embed, n=n_repetition)

    dwt_stegano.embed_data_in_audio(
        input_audio,
        output_audio,
        repeated_bits,
        wavelet_type="db4",
        decomposition_level=2,
    )
    print("Encrypted text embedded in", output_audio)
    print("Encrypted length (bytes):", enc_len)
    print("Encrypted length (bits):", len(bits))
    print("Repeated bit length:", len(repeated_bits))
    return len(repeated_bits), enc_len, n_repetition


def extract_and_decrypt(stego_audio, data_length, enc_len, n_repetition=5):
    extracted_bits = dwt_stegano.extract_data_from_audio(
        stego_audio, data_length, wavelet_type="db4", decomposition_level=2
    )
    recovered_bits = majority_vote(extracted_bits, n=n_repetition)

    # Find sync marker and extract encrypted message
    sync_marker = "1010101010101010"
    try:
        sync_idx = recovered_bits.index(sync_marker)
        length_bits = recovered_bits[sync_idx + 16 : sync_idx + 32]
        enc_len = int(length_bits, 2)
        enc_bits = recovered_bits[sync_idx + 32 : sync_idx + 32 + enc_len * 8]
        encrypted_bytes = bytes(
            int(enc_bits[i : i + 8], 2) for i in range(0, len(enc_bits), 8)
        )
        with open("keys/private.pem", "rb") as f:
            private_key = f.read()
        decrypted = decrypt_message(encrypted_bytes, private_key)
        print("Extracted and decrypted text:", decrypted)
    except Exception as e:
        print("Error extracting or decrypting text:", e)


if __name__ == "__main__":
    save_keys()
    bit_length, enc_len, n_repetition = encrypt_and_embed(
        "HALOOOOO ini teks testt CloudConvert converts your audio files online. Amongst many others, we support MP3, M4A, WAV and WMA. You can use the options to control audio quality and file size.",
        "audio/input.wav",
        "audio/stego.wav",
        n_repetition=5,
    )
    extract_and_decrypt("audio/stego.wav", bit_length, enc_len, n_repetition=5)
