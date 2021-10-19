import os
import openai
import speech_recognition as sr
import threading

from playsound import playsound
from digital_brain.computer_vision.model.utils.capture import Capture
from digital_brain.computer_vision.model.facial_detector import FaceDetector
from conversationalAI.models.text_to_speech import TextToSpeech
from conversationalAI.models.gpt_completion import Completion

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
    TextToSpeech.textToSpeechAudio("hello")
    # textToSpeechAudio("hello")
    filename = '../clean_audio.wav'
    playsound(filename)
    os.remove(filename)


# method that start the conversational application
def main_app():
    r = sr.Recognizer()
    try:
        while True:
            with sr.Microphone() as source:
                print("Please wait 1 second before speaking!")
                r.adjust_for_ambient_noise(source, duration=1)  # reduce noise
                audio_text = r.listen(source, timeout=4)
                print("Time over, thanks")

                text = r.recognize_google(audio_text)
                print("You: " + text)
                Completion.gptConversationalModel(text)

                if source is None:
                    continue

                # get goodbye from text and stop app
                # res = re.findall(r'\w+', text)
                # # print(res)
    except Exception as e:
        print(e)
        print("Conversation ended.")


# Method that starts the facial detection application
def start_cv():
    capture = Capture()
    face_detector = FaceDetector()

    while True:
        capture.start()
        _, bboxes = face_detector.find_faces(capture.frame)
        capture.show()

        if bboxes:
            detect_person_initial()

        if capture.wait_exit():
            break
    capture.cleanup()


if __name__ == '__main__':
    response = input("\nStart conversation (Yes or No)? ")
    if response[0] == "y":
        t1 = threading.Thread(target=start_cv)
        t2 = threading.Thread(target=main_app)

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    elif response[0] == "n":
        print("Application stopped. Good bye")