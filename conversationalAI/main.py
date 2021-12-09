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
    topics = ['intent', 'sentiment', 'kruidvat']
    print(topics)

    products = [
        {'ProductID': 1, 'Name': "L'ORÉAL PARIS MEN EXPERT HYDRA INTENSIVE 24H FACE CREAM", 'Size': '50ML', 'Price': 10.09, 'Skin Type': 'Dry'},
        {'ProductID': 2, 'Name': 'NIVEA MEN PROTECT & CARE MOISTURIZING FACE CREAM', 'Size': '75ML', 'Price': 10.99, 'Skin Type': 'Dry'},
        {'ProductID': 3, 'Name': "NIVEA MEN SENSITIVE MOISTURIZING FACE CREAM", 'Size': '75ML', 'Price': 11.99, 'Skin Type': 'Sensitive'},
        {'ProductID': 4, 'Name': "L'ORÉAL PARIS MEN EXPERT HYDRA SENSITIVE MOISTURIZING FACIAL CARE", 'Size': '50ML', 'Price': 15.15, 'Skin Type': 'Sensitive'},
        {'ProductID': 5, 'Name': "Andrélon Special Keratine Repair Shampoo", 'Size': '300ML', 'Price': 5.49, 'Hair Type': 'Dry and Fluffy'},
        {'ProductID': 6, 'Name': "Schwarzkopf Repair & Care Shampoo", 'Size': '400ML', 'Price': 2.59, 'Hair Type': 'Dry and Fluffy'},
        {'ProductID': 7, 'Name': "Kruidvat Sensation Tropical Shampoo", 'Size': '500ML', 'Price': 0.99, 'Hair Type': 'Normal'},
        {'ProductID': 8, 'Name': "John Frieda Frizz Ease Dream Curls Shampoo", 'Size': '250ML', 'Price': 11.99, 'Hair Type': 'Normal'}
    ]

    saleProducts = [
        {'ProductID': 1, 'Sale': '2nd half price'},
        {'ProductID': 3, 'Sale': '1 + 1 free'},
        {'ProductID': 5, 'Sale': '1 + 1 free'},
        {'ProductID': 7, 'Sale': '5 for 4.00 euros'}
    ]

    userProfile = [
        {'Gender': 'Male', 'Skin Type': 'Dry', 'Hair Type': 'Dry and Fluffy'}
    ]

    # TextToSpeech.textToSpeechAudio("Choose a demo. Intent or Sentiment Classification, or use-case Kruidvat. After choosing, speak when you hear the ding!")
    # filename = 'audio/clean_audio.wav'
    # playsound(filename)

    start_prompt = "The following is a conversation with Michelle Green, and she is a in-store AI virtual assistant for Kruidvat. " \
                   "Michelle always starts the conversation by asking the user how they are doing. " \
                   "Michelle is creative, helpful, smart, and very friendly. " \
                   "Michelle can give product recommendations strictly based on " + name + "'s user profile: " + str(userProfile) + ". " \
                   "Michelle recognizes the following sentiments: positive, neutral, and negative. " \
                   "Michelle recognizes the following intents: AddToCart, ConverseWithAI, UpdateCart, RemoveFromCart, SearchCart, ShowProduct, ShowCart, RecommendProduct. " \
                   "Michelle can only provide information and recommendations for this list of products identified by their ProductID " + str(products) + \
                   ". This is the list of products identified by ProductID on sale " + str(saleProducts) + \
                   ". Michelle will return a list of the product's name if asked, and she will add, remove, update, and search the shopping cart for " + name + ". " \
                   + name + "'s shopping cart is empty but is updated during the conversation with Michelle. " \
                   "Michelle will only add the items that " + name + " wants to cart, update the items he wants in the cart and she does not do something that " + name + " never asked her to do"

    sg.theme('DarkTeal')

    layout = [
        [sg.Text("Enter text here: "), sg.Input(key='-CONVO-'), sg.Button('Send')],
        [sg.Text("Use Voice Command"), sg.Button('Speak')],
        [sg.Button('Exit')],
        [sg.Output(size=(150, 20), key='-OUTPUT-')],
    ]

    window = sg.Window("In-Store AI Virtual Assistant for Kruidvat", layout)

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
        elif inputText == 'kruidvat':
            while True:
                event, values = window.read()
                text = values['-CONVO-']

                if text == 'stop':
                    return False
                else:
                    if event == "Exit" or event == sg.WIN_CLOSED:
                        break
                    elif event == "Speak":
                        voice_text = SpeechToText.speechToText("start")
                        text += voice_text

                        # print(text)

                        start_prompt += ". " + name + ": " + str(text) + ". Michelle:"
                        answer, start_prompt = GPTPlatform.conversationWithVirtualAssistant(start_prompt, name)

                        # print(start_prompt)

                        window['-OUTPUT-'].update("YOU: " + text + "\n" + "MICHELLE: " + answer)

                        with open('conversation_with_michelle_3.txt', 'w') as f:
                            f.write(start_prompt)
                    elif event == 'Send':
                        start_prompt += ". " + name + ": " + str(text) + ". Michelle:"
                        answer, start_prompt = GPTPlatform.conversationWithVirtualAssistant(start_prompt, name)

                        # print(start_prompt)

                        window['-OUTPUT-'].update("YOU: " + text + "\n" + "MICHELLE: " + answer)

                        with open('conversation_with_michelle_3.txt', 'w') as f:
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
