import speech_recognition as sr
from playsound import playsound


class SpeechToText:

    def __init__(self):
        pass

    # Method to run speech to text api from Google's speech API
    def speechToText(start):
        r = sr.Recognizer()
        print("Speak after the ding")

        with sr.Microphone() as source:
            playsound("audio/convo_prompt_2.mp3")
            r.adjust_for_ambient_noise(source, duration=1)  # reduce noise
            audio_text = r.listen(source, timeout=4)
            print("Time over, thanks")
            return r.recognize_google(audio_text)

