import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
import pyttsx3
import sys
import os
from contextlib import contextmanager

# Suppress ALSA warnings to keep output clean
@contextmanager
def suppress_stderr():
    stderr_fd = sys.stderr.fileno()
    old_stderr = os.dup(stderr_fd)
    null_fd = os.open(os.devnull, os.O_RDWR)
    try:
        os.dup2(null_fd, stderr_fd)
        yield
    finally:
        os.dup2(old_stderr, stderr_fd)
        os.close(null_fd)
        os.close(old_stderr)

r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

class SpeechToTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech-to-Text GUI")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
        self.text_area.pack(padx=10, pady=10)

        self.status_label = tk.Label(root, text="Press Start to begin listening", font=("Arial", 10))
        self.status_label.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Listening", command=self.start_listening)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Listening", command=self.stop_listening, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.listening = False

    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.status_label.config(text="🎧 Listening... Speak now (say 'exit' to quit)")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            threading.Thread(target=self.listen_loop, daemon=True).start()
            speak("Speech to text started. Say exit to quit.")

    def stop_listening(self):
        if self.listening:
            self.listening = False
            self.status_label.config(text="Stopped listening.")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            speak("Stopped listening.")

    def listen_loop(self):
        while self.listening:
            with sr.Microphone() as source:
                with suppress_stderr():
                    r.adjust_for_ambient_noise(source, duration=1.5)
                    r.dynamic_energy_adjustment_ratio = 1.5
                    audio = r.listen(source)

                try:
                    with suppress_stderr():
                        text = r.recognize_google(audio)

                    self.append_text(f">>> You said: \"{text}\"\n")
                    with open("output.txt", "a") as f:
                        f.write(text + "\n")
                    speak(f"You said: {text}")

                    if text.lower() in ("exit", "quit", "stop"):
                        self.append_text("Exiting...\n")
                        self.listening = False
                        self.root.after(0, self.stop_listening)
                        break

                except sr.UnknownValueError:
                    self.append_text("[!] Sorry, I couldn't understand that. Please try again.\n")
                except sr.RequestError:
                    self.append_text("[!] Could not request results from Google Speech Recognition service.\n")

    def append_text(self, message):
        self.text_area.insert(tk.END, message)
        self.text_area.see(tk.END)

def main():
    root = tk.Tk()
    app = SpeechToTextGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
