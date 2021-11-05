import os
import re
import time

import speech_recognition as sr
import threading

from playsound import playsound
from models.gpt import GPTPlatform
from digital_brain.computer_vision.model.utils.capture import Capture
from digital_brain.computer_vision.model.facial_detector import FaceDetector
from models.text_to_speech import TextToSpeech
from models.brand_sentiment_analysis import *

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


# method to get sentiment based speech converted to text - STT
def get_sentiment(sentiment):
    model = SentimentClassifier.load_sentiment_model()

    encoded_review = SentimentClassifier.tokenizer.encode_plus(
        sentiment,
        max_length=SentimentClassifier.MAX_LEN,
        add_special_tokens=True,
        return_token_type_ids=False,
        padding=True,
        return_attention_mask=True,
        return_tensors='pt',
        truncation=True,
    )

    input_ids = encoded_review['input_ids'].to(SentimentClassifier.device)
    attention_mask = encoded_review['attention_mask'].to(SentimentClassifier.device)

    output = model(input_ids, attention_mask)
    _, prediction = torch.max(output, dim=1)

    return SentimentClassifier.class_names[prediction]


# method that start the conversational application
def main_app():
    r = sr.Recognizer()

    topics = ['sustainability', 'customer support']
    print(topics)
    TextToSpeech.textToSpeechAudio("Please choose a topic. Sustainability or Customer Support. After choosing, speak when you hear the ding!")
    filename = 'audio/clean_audio.wav'
    playsound(filename)

    try:
        inputText = input('Choose a topic: ')
        if inputText == 'sustainability':
            while True:
                with sr.Microphone() as source:
                    print("Speak when you hear DING!!!")
                    playsound("audio/convo_prompt_2.mp3")
                    r.adjust_for_ambient_noise(source, duration=1)  # reduce noise
                    audio_text = r.listen(source, timeout=4)
                    print("Time over, thanks")
                    text = r.recognize_google(audio_text)
                    print("You: " + text)

                    # text = input("Enter text here: ")
                    # get goodbye from text and stop app
                    res = re.findall(r'\w+', text)
                    if "goodbye" in res and len(res) == 1:
                        break

                    user_sentiment_on_brands = get_sentiment(text) + ". " + text
                    print(user_sentiment_on_brands)
                    GPTPlatform.brandDetectionUsingSentiment(user_sentiment_on_brands)

                    if source is None:
                        continue
        elif inputText == 'customer support':
            TextToSpeech.textToSpeechAudio("I can't give you any support at this moment.")
            filename = 'audio/clean_audio.wav'
            playsound(filename)
            os.remove(filename)
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
