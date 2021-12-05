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
from tkinter import *
import PySimpleGUI as sg


# Method using ThreadPoolExecutor to run tasks concurrently
def run_conversational_tasks(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.running()


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


# method that start the conversational application
def main_app(name):
    topics = ['intent', 'sentiment', 'conversation']
    print(topics)

    products = [
        {'Name': 'SLIM FIT JEANS', 'Price': 25, 'Colors': ['blue', 'light blue', 'black', 'gray', 'light brown']},
        {'Name': 'LOOSE FIT JEANS', 'Price': 35, 'Colors': ['navy blue', 'taupe brown', 'black', 'blue']},
        {'Name': 'BASIC SKINNY JEANS', 'Price': 45, 'Colors': ['light blue', 'mid-blue', 'black', 'blue', 'charcoal']},
        {'Name': 'CARGO JEANS WITH SEAM DETAILS', 'Price': 19, 'Colors': ['khaki', 'gray', 'black']}]

    # TextToSpeech.textToSpeechAudio("Choose a demo. Intent or Sentiment Classification, or just a conversation with your virtual assistant. After choosing, speak when you hear the ding!")
    # filename = 'audio/clean_audio.wav'
    # playsound(filename)

    start_prompt = "The following is a conversation with Michelle Green, and she is a in-store virtual assistant for " \
                   "Zara. Michelle is helpful, fashionable, smart, and very friendly.  Michelle knows that " + name + \
                   "favorite colors are blue and black. Michelle will give product recommendations based on " + name + "'s " \
                   "color preferences. " + name + "'s shopping cart is empty. Michelle recognizes the following sentiments: " \
                   "positive, neutral, and negative. Michelle recognizes the following intents: AddToCart, " \
                   "ConverseWithAI, UpdateCart, RemoveFromCart, SearchCart, ShowProduct, RecommendProduct. " \
                   "Michelle can only provide information and recommendations for these products " + str(products) + \
                   "Michelle will return a list of the product's name if asked, and she will add, remove, update, " \
                   "and search cart for " + name + ". "

    layout = [
        [sg.Text("Enter text here: "), sg.Input(key='-CONVO-')],
        [sg.Button('Send'), sg.Button('Exit')],
        [sg.Output(size=(150, 20), key='-OUTPUT-')],
    ]
    sg.theme('DarkPurple6')
    window = sg.Window("Demo", layout)

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
        elif inputText == 'conversation':
            while True:
                event, values = window.read()
                text = values['-CONVO-']

                # text = SpeechToText.speechToText("start")

                if text == 'stop':
                    return False
                else:
                    if event == "Exit" or event == sg.WIN_CLOSED:
                        break

                    start_prompt += ". " + name + ": " + SentimentClassifier.get_sentiment(text) + ". " + str(text) + ". Michelle:"
                    answer, start_prompt = GPTPlatform.conversationWithVirtualAssistant(start_prompt, name)

                    window['-OUTPUT-'].update("You: " + text + "\n\n" + "Michelle: " + answer)

                    with open('conversation_with_michelle_2.txt', 'w') as f:
                        f.write(start_prompt)
    except Exception as e:
        print(e)
        print("Conversation ended.")


if __name__ == '__main__':
    name = input("Enter your name: ")
    main_app(name)
    
    # run_conversational_tasks([
    #     # start_cv(),
    #     main_app(name),
    # ])
