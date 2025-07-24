import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import io
import threading

# Initialize recognizer
recognizer = sr.Recognizer()
fs = 16000  # Sample rate
recording = []
is_recording = False

def start_recording():
    global recording, is_recording
    is_recording = True
    recording = []
    status_label.config(text="🎙️ Recording... Click STOP when done.")
    text_output.delete("1.0", tk.END)

    def callback(indata, frames, time, status):
        if is_recording:
            recording.append(indata.copy())

    # Start the audio stream in a background thread
    def record_audio():
        with sd.InputStream(samplerate=fs, channels=1, dtype='float32', callback=callback):
            while is_recording:
                sd.sleep(100)

    threading.Thread(target=record_audio).start()

def stop_recording():
    global is_recording
    is_recording = False
    status_label.config(text="✅ Recording stopped. Click TRANSCRIBE.")

def transcribe_audio():
    global recording
    if not recording:
        messagebox.showerror("Error", "No audio recorded.")
        return

    status_label.config(text="🧠 Transcribing...")

    try:
        # Concatenate all chunks
        audio_np = np.concatenate(recording, axis=0)

        # Convert float32 to int16 PCM
        audio_int16 = np.int16(audio_np * 32767)

        # Save to buffer
        buffer = io.BytesIO()
        wav.write(buffer, fs, audio_int16)
        buffer.seek(0)

        # Transcribe with SpeechRecognition
        with sr.AudioFile(buffer) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, text)
        status_label.config(text="✅ Transcription complete.")

    except sr.UnknownValueError:
        messagebox.showerror("Error", "Speech was unintelligible.")
    except sr.RequestError:
        messagebox.showerror("Error", "Could not reach the speech API.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# === GUI SETUP ===
root = tk.Tk()
root.title("🎤 Voice Transcription App")
root.geometry("600x400")

tk.Label(root, text="Start recording, speak freely, stop, and transcribe:", font=("Helvetica", 14)).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Button(frame, text="🔴 Start Recording", command=start_recording, bg="lightcoral", font=("Helvetica", 12)).grid(row=0, column=0, padx=10)
tk.Button(frame, text="⏹️ Stop", command=stop_recording, bg="orange", font=("Helvetica", 12)).grid(row=0, column=1, padx=10)
tk.Button(frame, text="📄 Transcribe", command=transcribe_audio, bg="lightgreen", font=("Helvetica", 12)).grid(row=0, column=2, padx=10)

text_output = tk.Text(root, height=10, width=70, wrap=tk.WORD, font=("Helvetica", 12))
text_output.pack(pady=15)

status_label = tk.Label(root, text="", font=("Helvetica", 10), fg="gray")
status_label.pack()

root.mainloop()
