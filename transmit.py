import numpy as np
import pygame
import time
import tkinter as tk

# Set up audio parameters
RATE = 44100  # Sample rate (samples per second)
DURATION = 0.01  # Fixed duration per bit

# Frequencies for binary encoding
FREQ_1 = 17000  # Frequency for binary 1 heard as 2900-3500hz
FREQ_0 = 20000  # Frequency for binary 0 heard as 3900-4500hz

# Initialize pygame mixer
pygame.mixer.init(frequency=RATE, size=-16, channels=1, buffer=512)

def generate_tone(frequency, duration):
    """Generate a sound array for a given frequency and duration."""
    t = np.linspace(0, duration, int(RATE * duration), endpoint=False)
    wave_data = np.sin(2 * np.pi * frequency * t) * 32767  # 16-bit PCM scale
    wave_data = wave_data.astype(np.int16)  # Convert to int16
    return pygame.mixer.Sound(wave_data.tobytes())

# Pre-generate sounds for fast playback
sound_0 = generate_tone(FREQ_0, DURATION)
sound_1 = generate_tone(FREQ_1, DURATION)

def play_sine_wave(sound):
    """Play a generated sine wave instantly."""
    sound.play()
    time.sleep(DURATION)  # Ensure it plays fully

def text_to_binary(text):
    """Convert text to binary (8-bit per character)."""
    return ''.join(format(ord(char), '08b') for char in text)

def send_binary():
    """Convert text input to binary and send it via sound signals."""
    text = entry.get()
    binary_data = text_to_binary(text)
    
    for bit in binary_data:
        if bit == '0':
            play_sine_wave(sound_0)
        else:
            play_sine_wave(sound_1)
    
    status_label.config(text=f"Sent: {binary_data}")

# GUI Setup
root = tk.Tk()
root.title("Binary Text Sender")

# Input field
entry_label = tk.Label(root, text="Enter text:")
entry_label.pack()
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Send button
send_button = tk.Button(root, text="Send", command=send_binary, width=20, height=2)
send_button.pack(pady=10)

# Status label
status_label = tk.Label(root, text="")
status_label.pack(pady=5)

# Run the GUI
root.mainloop()
