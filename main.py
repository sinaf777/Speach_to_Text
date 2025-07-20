import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
engine = pyttsx3.init()

def record_text():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
                text = r.recognize_google(audio)
                print(f"You said: {text}")
                return text

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")

def output_text(text):
    with open("output.txt", "a") as f:
        f.write(text + "\n")

def speak(text):
    engine.say(text)
    engine.runAndWait()

try:
    while True:
        text = record_text()
        output_text(text)
        speak("Text recorded.")
        print("Wrote text.")

except KeyboardInterrupt:
    print("\n[!] Exiting gracefully.")
