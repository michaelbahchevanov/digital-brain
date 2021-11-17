import os

from playsound import playsound
from models.gpt import GPTPlatform
from digital_brain.computer_vision.model.utils.capture import Capture
from digital_brain.computer_vision.model.facial_detector import FaceDetector
from models.text_to_speech import TextToSpeech
from models.speech_to_text import SpeechToText
from models.brand_sentiment_analysis import *
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures


# Wrapper to run a method once
def run_once(trigger):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return trigger(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


# Method to initiate conversation with Michelle Green
@run_once
def detect_person_initial():
    TextToSpeech.textToSpeechAudio("Hey there!")
    filename = 'audio/clean_audio.wav'
    playsound(filename)
    os.remove(filename)


# method that start the conversational application
def main_app():
    topics = ['intent', 'sentiment']
    print(topics)

    TextToSpeech.textToSpeechAudio("Choose a demo. Intent Classification or Sentiment Classification. After choosing, speak when you hear the ding!")
    filename = 'audio/clean_audio.wav'
    playsound(filename)

    try:
        inputText = input('Choose a topic: ')
        if inputText == 'intent':
            while True:
                text = SpeechToText.speechToText("start")
                if text == 'stop':
                    return False
                else:
                    user_intent = GPTPlatform.intentClassifier(text) + " " + text
                    GPTPlatform.conversationWithIntent(user_intent)
        elif inputText == 'sentiment':
            while True:
                text = SpeechToText.speechToText("start")
                if text == 'stop':
                    return False
                else:
                    user_sentiment_on_brands = SentimentClassifier.get_sentiment(text) + ". " + text
                    GPTPlatform.brandDetectionUsingSentiment(user_sentiment_on_brands)
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


# Method using ThreadPoolExecutor to run tasks concurrently
def run_conversational_tasks(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.done()


if __name__ == '__main__':
    run_conversational_tasks([
        start_cv(),
        main_app(),
    ])
