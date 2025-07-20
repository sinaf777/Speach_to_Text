import speech_recognition as sr
import pyttsx3
import sys

r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def record_text():
    with sr.Microphone() as source:
        print("\n🎧 Listening... Speak now (say 'exit' to quit)")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.RequestError:
        print("[!] Could not request results from Google Speech Recognition service.")
        return None
    except sr.UnknownValueError:
        print("[!] Sorry, I couldn't understand that. Please try again.")
        return None

def main():
    print("=== Speech-to-Text Interactive Session ===")
    speak("Speech to text started. Say exit to quit.")

    while True:
        text = record_text()
        if text:
            print(f">>> You said: \"{text}\"")
            with open("output.txt", "a") as f:
                f.write(text + "\n")
            speak(f"You said: {text}")

            if text.lower() in ("exit", "quit", "stop"):
                print("Exiting... Goodbye!")
                speak("Goodbye!")
                sys.exit()

if __name__ == "__main__":
    main()
