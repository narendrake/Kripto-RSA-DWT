import soundfile as sf
import numpy as np


def calculate_psnr(original, stego):
    mse = np.mean((original - stego) ** 2)
    if mse == 0:
        return float("inf")
    max_pixel = np.max(np.abs(original))
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr


if __name__ == "__main__":
    # Change these paths if needed
    original_path = "audio/input.wav"
    stego_path = "audio/stego.wav"

    # Read audio files
    original, sr1 = sf.read(original_path)
    stego, sr2 = sf.read(stego_path)

    print(f"Original shape: {original.shape}")
    print(f"Stego shape:    {stego.shape}")

    # Convert both to mono if needed
    if original.ndim > 1:
        original = original[:, 0]
    if stego.ndim > 1:
        stego = stego[:, 0]

    # Truncate to the same length
    min_len = min(len(original), len(stego))
    original = original[:min_len]
    stego = stego[:min_len]

    # Ensure same sample rate
    if sr1 != sr2:
        print("Sample rates do not match!")
        exit(1)

    psnr = calculate_psnr(original, stego)
    print(f"PSNR between {original_path} and {stego_path}: {psnr:.2f} dB")
