import tkinter as tk
from tkinter import filedialog, messagebox
import os
import io
import sys

import dwt_stegano
from main import (
    save_keys,
    encrypt_and_embed,
    extract_and_decrypt,
    encrypt_message,
)


class SteganoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA + DWT Audio Steganography")
        self.root.configure(padx=10, pady=10)

        # Make columns 1, 2, 3 expandable
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=0)
        self.root.columnconfigure(3, weight=0)

        # Message input
        tk.Label(root, text="Message to Hide:").grid(
            row=0, column=0, sticky="e", pady=3
        )
        self.message_entry = tk.Entry(root)
        self.message_entry.grid(
            row=0, column=1, columnspan=3, padx=5, pady=3, sticky="ew"
        )

        # Input audio
        tk.Label(root, text="Input Audio:").grid(row=1, column=0, sticky="e", pady=3)
        self.input_audio_var = tk.StringVar()
        tk.Entry(root, textvariable=self.input_audio_var).grid(
            row=1, column=1, padx=5, pady=3, sticky="ew"
        )
        tk.Button(root, text="Browse", command=self.browse_input_audio).grid(
            row=1, column=2, padx=2, pady=3, sticky="ew"
        )

        # Output audio
        tk.Label(root, text="Stego (Output) Audio:").grid(
            row=2, column=0, sticky="e", pady=3
        )
        self.output_audio_var = tk.StringVar()
        tk.Entry(root, textvariable=self.output_audio_var).grid(
            row=2, column=1, padx=5, pady=3, sticky="ew"
        )
        tk.Button(root, text="Browse", command=self.browse_output_audio).grid(
            row=2, column=2, padx=2, pady=3, sticky="ew"
        )

        # Buttons
        tk.Button(root, text="Generate Keys", command=self.generate_keys).grid(
            row=3, column=0, pady=10, sticky="ew"
        )
        tk.Button(root, text="Embed Message", command=self.embed_message).grid(
            row=3, column=1, pady=10, sticky="ew"
        )
        tk.Button(root, text="Extract Message", command=self.extract_message).grid(
            row=3, column=2, pady=10, sticky="ew"
        )

        # Encrypted message display
        tk.Label(root, text="Encrypted Message:").grid(
            row=4, column=0, sticky="e", pady=3
        )
        self.encrypted_message_var = tk.StringVar()
        tk.Entry(root, textvariable=self.encrypted_message_var, state="readonly").grid(
            row=4, column=1, columnspan=3, padx=5, pady=3, sticky="ew"
        )

        # Extracted message display
        tk.Label(root, text="Extracted Message:").grid(
            row=5, column=0, sticky="e", pady=3
        )
        self.extracted_message_var = tk.StringVar()
        tk.Entry(root, textvariable=self.extracted_message_var, state="readonly").grid(
            row=5, column=1, columnspan=3, padx=5, pady=3, sticky="ew"
        )

    def browse_input_audio(self):
        filename = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if filename:
            self.input_audio_var.set(filename)

    def browse_output_audio(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".wav", filetypes=[("WAV files", "*.wav")]
        )
        if filename:
            self.output_audio_var.set(filename)

    def generate_keys(self):
        save_keys()
        messagebox.showinfo("Info", "RSA keys generated and saved in /keys folder.")

    def embed_message(self):
        msg = self.message_entry.get()
        input_audio = self.input_audio_var.get()
        output_audio = self.output_audio_var.get()
        if not (msg and input_audio and output_audio):
            messagebox.showerror("Error", "Please fill all fields.")
            return
        try:
            # Encrypt only (do not embed yet)
            with open("keys/public.pem", "rb") as f:
                public_key = f.read()
            encrypted = encrypt_message(msg, public_key)
            # Show as hex
            self.encrypted_message_var.set(encrypted.hex())

            # Now embed as usual
            bit_length, enc_len, n_repetition = encrypt_and_embed(
                msg, input_audio, output_audio, n_repetition=5
            )
            messagebox.showinfo("Success", f"Message embedded in {output_audio}")
        except Exception as e:
            messagebox.showerror("Error", f"Embedding failed: {e}")

    def extract_message(self):
        output_audio = self.output_audio_var.get()
        if not output_audio:
            messagebox.showerror("Error", "Please select the stego audio file.")
            return
        try:
            n_repetition = 5
            bit_length = 100000  # Large enough to cover the message
            enc_len = None  # Let extract_and_decrypt handle length extraction
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()
            extract_and_decrypt(output_audio, bit_length, enc_len, n_repetition)
            sys.stdout = old_stdout
            result = mystdout.getvalue()
            if "Extracted and decrypted text:" in result:
                extracted = result.split("Extracted and decrypted text:")[-1].strip()
                self.extracted_message_var.set(extracted)
            else:
                self.extracted_message_var.set("Extraction failed.")
        except Exception as e:
            messagebox.showerror("Error", f"Extraction failed: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, False)  # Only allow horizontal resizing
    root.minsize(600, 220)  # Set minimum window size
    root.maxsize(1000, 220)  # Set maximum window size (width only)
    app = SteganoGUI(root)
    root.mainloop()
