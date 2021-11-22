import speech_recognition as sr
from playsound import playsound
import re


class SpeechToText:

    def __init__(self):
        pass

    # Method to run speech to text api from Google's speech API
    def speechToText(start):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # print("Speak when you hear DING!!!")
            # playsound("audio/convo_prompt_2.mp3")
            # r.adjust_for_ambient_noise(source, duration=1)  # reduce noise
            # audio_text = r.listen(source, timeout=4)
            # print("Time over, thanks")
            # text = r.recognize_google(audio_text)
            # print("You: " + text)

            text = input("Enter text here: ")
            print("You: " + text)

            # # get goodbye from text and stop running
            res = re.findall(r'\w+', text)
            if "goodbye" in res and len(res) == 1:
                return "stop"

            # stop_listening = r.listen_in_background(m, callback)
            # print(stop_listening)
            return text

