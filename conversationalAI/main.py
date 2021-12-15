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
import os.path
import PIL.Image
import io
import base64
from datetime import datetime


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

# Method to convert image to bytes. This method helps
# with displaying images in python
def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


# Method to send API request to openAI and save conversation history
def conversationLogic(text, start_prompt, name, window):
    start_prompt += ". " + name + ": " + str(text) + ". Michelle:"
    answer, start_prompt = GPTPlatform.conversationWithVirtualAssistant(start_prompt, name)

    # print(start_prompt)

    window['-OUTPUT-'].update("YOU: " + text + "\n" + "MICHELLE: " + answer)


    with open("conversation_with_michelle_4" + "-" + datetime.now().strftime("%d/%m/%Y %H:%M:%S")+".txt", 'w') as f:
        f.write(start_prompt)


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
        {'ProductID': 5, 'Sale': '2 + 1 free'},
        {'ProductID': 7, 'Sale': '3 + 1 free'}
    ]

    userProfile = [
        {'Gender': 'Male', 'Skin Type': 'Dry', 'Hair Type': 'Dry and Fluffy'}
    ]

    availabilityStore = [
        {"City": "Eindhoven", "Location":["Binnenstad", "Bergen", "Witte Dame"]}
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
                   ". In between the conversation Michelle tells " + name + " random facts about Kruidvat. " + \
                   "Michelle can let " + name + " know where in the city " + str(availabilityStore) + " they can find the product in their shopping cart" + \
                   ". Michelle will return a list of the product's name if asked, and she will add, remove, update, and search the shopping cart for " + name + ". " \
                   + name + "'s shopping cart is empty but is updated during the conversation with Michelle. " \
                   "Michelle will only add the items that " + name + " wants to cart, update the items he wants in the cart. " \
                   "Michelle listens carefully to " + name + " needs and does exactly what he asked her to do"

    sg.theme('DarkTeal')
    filename = "audio/michelle_image.png"

    layout = [
        [sg.Image(data=convert_to_bytes(filename, resize=(300, 300)), key='-IMAGE-')],
        [sg.Text("Enter text here: "), sg.Input(key='-CONVO-'), sg.Button('Send')],
        [sg.Text("Use Voice Command"), sg.Button('Speak')],
        [sg.Button('Exit')],
        [sg.Output(size=(150, 20), key='-OUTPUT-')],
    ]

    window = sg.Window("In-Store AI Virtual Assistant for Kruidvat", layout, resizable=True)

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

                        conversationLogic(text, start_prompt, name, window)
                    elif event == 'Send':
                        conversationLogic(text, start_prompt, name, window)
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
