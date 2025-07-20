import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()

def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                print("Listening... 🎤")
                r.adjust_for_ambient_noise(source2, duration=0.5)
                audio2 = r.listen(source2)

                MyText = r.recognize_google(audio2)
                return MyText

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
    return

def output_text(text):
    with open("output.txt", "a") as f:
        f.write(text + "\n")

while True:
    text = record_text()

    if text:
        print("You said:", text) 
        output_text(text)         
