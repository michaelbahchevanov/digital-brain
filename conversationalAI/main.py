import os
from playsound import playsound
from models.gpt import GPTPlatform
from digital_brain.computer_vision.model.utils.capture import Capture
from digital_brain.computer_vision.model.facial_detector import FaceDetector
from models.text_to_speech import TextToSpeech
from models.speech_to_text import SpeechToText
from models.sentiment_analysis import *
from models.dummy_data import DummyData
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import PySimpleGUI as sg
import os.path
import PIL.Image
import io
import base64
from datetime import datetime
from pynput.keyboard import Key, Listener, Controller
import geocoder
import re


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
    try:
        start_prompt += ". " + name + ": " + str(text) + ". Michelle:"
        answer, start_prompt = GPTPlatform.conversationWithVirtualAssistant(start_prompt, name)

        window['-OUTPUT-'].update("YOU: " + text + "\n" + "MICHELLE: " + answer)
        window['-CONVO-'].update("")

        # " + "-" + datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"
        with open("conversation_with_michelle_4.txt", 'w') as f:
            f.write(start_prompt)
    except Exception as e:
        print(e)


# Method to get location of city
def getCity():
    g = geocoder.ip('me')
    print(g.city)
    Eindhoven = [
        "Winkelcentrum Woensel", "Strijpsestraat"
    ]

    Tilburg = [
        "Pieter Vredeplein", "Besterdring", "Heuvelstraat"
    ]

    if g.city == "Amsterdam":
        return Eindhoven
    elif g.city == "Tilburg":
        return Tilburg


# Method contains the dialog for the conversation logic
def main_app(name, gender, skin_type, hair_type):

    saleProducts = [
        {'ProductID': 1, 'Sale': '2nd half price'},
        {'ProductID': 3, 'Sale': '1 + 1 free'},
        {'ProductID': 5, 'Sale': '2 + 1 free'},
        {'ProductID': 7, 'Sale': '3 + 1 free'}
    ]

    userProfile = [
        {'Gender': gender, 'Skin Type': skin_type, 'Hair Type': hair_type}
    ]

    start_prompt = "The following is a conversation with Michelle Green, and she is an AI assistant and a AI salesperson for Kruidvat. " \
                    "Michelle starts the conversation by greeting the user by their name. Michelle is creative, talkative, helpful, smart, and very friendly. " \
                    "Michelle gives product recommendations strictly based on " + name + "'s user profile: " + str(userProfile) + ". Michelle is emotionally " \
                    "intelligent and understands the user's intent. Michelle will give information about Kruidvat's " + str(DummyData.getProducts(gender, skin_type, hair_type)) + " that are " \
                    "identified by their ProductID. Michelle will inform the user that these products:" + str(saleProducts) + " are currently on sale. " + \
                    "Due to the COVID-19 measures set by the Government, Michelle will inform the user that it is not possible to shop in the store and " \
                    "that Kruidvat is allowing for customers to Click & Collect. Michelle can let " + name + " know the opening hours are 8 AM to 6 PM" \
                    " are for the stores located in " + str(getCity()) + ". The user can find the products in their shopping cart at these locations as well"\
                    ". Michelle will return a list of the product's name if asked, and she will add, remove, update, and search the shopping cart for " + name + ". " \
                    + name + "'s shopping cart is empty but is updated during the conversation with Michelle"

    sg.theme('DarkRed1')
    filename = "audio/michelle_image.png"

    layout = [
        [sg.Image(data=convert_to_bytes(filename, resize=(300, 300)), key='-IMAGE-')],
        [sg.Text("Enter text here: "), sg.Input(key='-CONVO-'), sg.Text('press Enter to send')],
        [sg.Text("Use Voice Command"), sg.Button('Speak')],
        [sg.Button('Exit')],
        [sg.Output(size=(80, 20), key='-OUTPUT-')],
    ]

    window = sg.Window("AI Assistant for Kruidvat", layout, return_keyboard_events=True, resizable=True) #use_default_focus=False

    try:
        while True:
            event, values = window.read()
            text = values['-CONVO-']

            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "Speak":
                voice_text = SpeechToText.speechToText("start")
                text += voice_text

                start_prompt += ". " + name + ": " + str(text) + ". Michelle:"
                answer, start_prompt = GPTPlatform.conversationWithVirtualAssistant(start_prompt, name)

                window['-OUTPUT-'].update("YOU: " + text + "\n" + "MICHELLE: " + answer)
                window['-CONVO-'].update("")

                with open("conversation_with_michelle_4.txt", 'w') as f:
                    f.write(start_prompt)

            elif event == 'Return:36':
                # # Change image based on user emotional state
                # if SentimentClassifier.get_sentiment(text) == "neutral":
                #     window['-IMAGE-'].update(data=convert_to_bytes("audio/Pngtree_cool_face.png", resize=(100, 100)))
                # elif SentimentClassifier.get_sentiment(text) == "positive":
                #     window['-IMAGE-'].update(data=convert_to_bytes("audio/Pngtree_happy_face.png", resize=(100, 100)))
                # elif SentimentClassifier.get_sentiment(text) == "negative":
                #     window['-IMAGE-'].update("audio/cry_face.gif")

                # checkout = 'checkout'
                # go_to_checkout = re.findall(checkout, text)
                #
                # if go_to_checkout:
                #     # event2, values2 = window2.read()
                #     print(go_to_checkout)

                start_prompt += ". " + name + ": " + str(text) + ". Michelle:"
                answer, start_prompt = GPTPlatform.conversationWithVirtualAssistant(start_prompt, name)

                window['-OUTPUT-'].update("YOU: " + text + "\n" + "MICHELLE: " + answer)
                window['-CONVO-'].update("")

                with open("conversation_with_michelle_4.txt", 'w') as f:
                    f.write(start_prompt)

    except Exception as e:
        print(e)
        print("Conversation ended.")


if __name__ == '__main__':
    TextToSpeech.textToSpeechAudio("Hey there, before we start let's build your profile for the best experience.")
    filename = 'audio/clean_audio.wav'
    playsound(filename)
    os.remove(filename)
    name = input("Enter your name: ")
    gender = input("Enter your gender (man, woman): ")
    skin_type = input("Enter your skin type (dry or sensitive): ")
    hair_type = input("Enter your hair type (dry or normal): ")
    main_app(name, gender, skin_type, hair_type)


def main():
    window1, window2 = make_win1(), make_win2()

    window2.move(window1.current_location()[0], window1.current_location()[1]+220)

    while True:             # Event Loop
        window, event, values = sg.read_all_windows()

        if window == sg.WIN_CLOSED:     # if all windows were closed
            break
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            if window == window2:       # if closing win 2, mark as closed
                window2 = None
            elif window == window1:     # if closing win 1, mark as closed
                window1 = None
        elif event == 'Reopen':
            if not window2:
                window2 = make_win2()
                window2.move(window1.current_location()[0], window1.current_location()[1] + 220)
        elif event == '-IN-':
            output_window = window2 if window == window1 else window1
            if output_window:           # if a valid window, then output to it
                output_window['-OUTPUT-'].update(values['-IN-'])
            else:
                window['-OUTPUT-'].update('Other window is closed')


if __name__ == '__main__':
    main()