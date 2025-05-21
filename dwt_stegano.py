import numpy as np
import pywt
import soundfile as sf


def process_audio(
    audio_path,
    data_bits=None,
    wavelet_type="db1",
    decomposition_level=1,
    scale_factor=0.001,
):
    """
    Handles both the embedding and extraction processes depending on the presence of data_bits.
    """
    audio_data, sample_rate = sf.read(audio_path)
    if len(audio_data.shape) > 1 and audio_data.shape[1] > 1:
        audio_data = audio_data[:, 0]  # Use the first channel for stereo audio

    # Apply DWT to the audio data
    coefficients = pywt.wavedec(audio_data, wavelet_type, level=decomposition_level)

    if data_bits:
        # Embed data into wavelet coefficients
        detail_coeffs = coefficients[1].copy()
        for i in range(len(data_bits)):
            coeff_abs = abs(detail_coeffs[i])
            remainder = coeff_abs % (2 * scale_factor)
            target_remainder = scale_factor if data_bits[i] == "1" else 0
            adjustment = target_remainder - remainder
            sign = 1 if detail_coeffs[i] >= 0 else -1
            detail_coeffs[i] = sign * (coeff_abs + adjustment)
        coefficients[1] = detail_coeffs

        # Reconstruct the audio from modified coefficients
        reconstructed_audio = pywt.waverec(coefficients, wavelet_type)
        return reconstructed_audio, sample_rate

    else:
        # Extract bits from wavelet coefficients
        extracted_bits = ""
        detail_coeffs = coefficients[1]
        for coeff in detail_coeffs:
            coeff_value = abs(coeff)
            remainder = coeff_value % (2 * scale_factor)
            if scale_factor * 0.4 <= remainder <= scale_factor * 1.6:
                extracted_bits += "1"
            else:
                extracted_bits += "0"
        return extracted_bits


def embed_data_in_audio(
    audio_path,
    output_path,
    data_bits,
    wavelet_type="db1",
    decomposition_level=1,
    scale_factor=0.001,
):
    """
    Embed data bits into the audio file and save the modified audio.
    """
    reconstructed_audio, sample_rate = process_audio(
        audio_path, data_bits, wavelet_type, decomposition_level, scale_factor
    )
    sf.write(output_path, reconstructed_audio, sample_rate)
    return True


def extract_data_from_audio(
    stego_audio_path,
    num_bits,
    wavelet_type="db1",
    decomposition_level=1,
    scale_factor=0.001,
):
    """
    Extract embedded data bits from the stego audio file.
    """
    extracted_bits = process_audio(
        stego_audio_path,
        wavelet_type=wavelet_type,
        decomposition_level=decomposition_level,
        scale_factor=scale_factor,
    )
    return extracted_bits[:num_bits]
