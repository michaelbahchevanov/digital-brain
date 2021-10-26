import os
import re
import time

import openai
import speech_recognition as sr
import threading

from playsound import playsound

from conversationalAI.models.gpt import GPTPlatform
from digital_brain.computer_vision.model.utils.capture import Capture
from digital_brain.computer_vision.model.facial_detector import FaceDetector
from models.text_to_speech import TextToSpeech

openai.api_key = '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'


# Wrapper to run a method once
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


# Method to initiate conversation with Michelle Green
@run_once
def detect_person_initial():
    TextToSpeech.textToSpeechAudio("Hello there!")
    filename = '../clean_audio.wav'
    playsound(filename)
    os.remove(filename)


# method that start the conversational application
def main_app():
    r = sr.Recognizer()

    topics = ['sustainability', 'customer support']
    print(topics)
    TextToSpeech.textToSpeechAudio("Please choose one of the following topics. Sustainability or customer support")
    filename = '../clean_audio.wav'
    playsound(filename)

    try:

        # os.remove(filename)
        inputText = input('Choose a topic: ')
        if inputText == 'sustainability':
            while True:
                with sr.Microphone() as source:
                    print("Speak when you hear DING!!!")
                    playsound("convo_prompt_2.mp3")
                    r.adjust_for_ambient_noise(source, duration=1)  # reduce noise
                    audio_text = r.listen(source, timeout=4)
                    print("Time over, thanks")

                    text = r.recognize_google(audio_text)
                    print("You: " + text)

                    # get goodbye from text and stop app
                    res = re.findall(r'\w+', text)
                    if "goodbye" in res and len(res) == 1:
                        break

                    GPTPlatform.gptConversationalModel(text)

                    if source is None:
                        continue
        elif inputText == 'customer support':
            TextToSpeech.textToSpeechAudio("I can't give you any support at the moment.")
            filename = '../clean_audio.wav'
            playsound(filename)
            # os.remove(filename)
            return
    except Exception as e:
        print(e)
        print("Conversation ended.")


# Method that starts the facial detection application
def start_cv():
    capture = Capture(-1)
    face_detector = FaceDetector()

    while True:
        capture.start()
        _, bboxes = face_detector.find_faces(capture.frame)

        if bboxes:
            detect_person_initial()
            return True

        if capture.wait_exit():
            break

    capture.cleanup()


def main():
    while True:
        init = start_cv()
        if init:
            time.sleep(2)
            app_thread = threading.Thread(target=main_app)
            app_thread.start()
            end = app_thread.join()

            if not end:
                print('ENDED')
                break
            else:
                continue


if __name__ == '__main__':
    main()



