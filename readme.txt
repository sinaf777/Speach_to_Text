To run use this command in your terminal 

cd /home/s1n4f/Documents/py/Python-Experiments/Speach_to_Text
python -m venv .venv
source .venv/bin/activate
pip install SpeechRecognition pyttsx3
sudo pacman -S portaudio tk
pip install pyaudio
python gui_speech_to_text.py
