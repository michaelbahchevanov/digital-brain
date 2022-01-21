import os
from playsound import playsound
from models.gpt import GPTPlatform
from models.text_to_speech import TextToSpeech
from models.speech_to_text import SpeechToText
from models.sentiment_analysis import *
from models.dummy_data import DummyData
import PySimpleGUI as sg
import PIL.Image
import io
import base64


# Method to convert image to bytes. This method helps with displaying images in python
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


# Method contains the GUI logic integrated with the platforms' NLP techniques
def main_app(name, gender, skin_type, hair_type):

    # Prompt engineering/designing
    start_prompt = "The following is a conversation with Michelle Green, and she is an AI assistant and a AI salesperson for Kruidvat. " \
                    "Michelle starts the conversation by greeting the user by their name. Michelle is creative, helpful, smart, and very friendly. " \
                    "Michelle gives product recommendations strictly based on " + name + "'s user profile: " + str(DummyData.buildUserProfile(gender, skin_type, hair_type)) + "."

    sg.theme('DarkRed1')
    filename = "images/michelle_image.png"

    layout = [
        [sg.Image(data=convert_to_bytes(filename, resize=(300, 300)), key='-IMAGE-')],
        [sg.Text("Enter text here: "), sg.Input(key='-CONVO-'), sg.Text('press Enter to send')],
        [sg.Text("Use Voice Command"), sg.Button('Speak')],
        [sg.Button('Exit')],
        [sg.Output(size=(80, 20), key='-OUTPUT-')],
    ]

    window = sg.Window("AI Assistant for Kruidvat", layout, return_keyboard_events=True, resizable=True)

    try:
        while True:
            event, values = window.read()
            text = values['-CONVO-']

            if event in ["Exit", sg.WIN_CLOSED]:
                break
            elif event == "Speak": # Speak button
                voice_text = SpeechToText.speechToText("start")
                text += voice_text

                start_prompt += ". " + name + ": " + str(text) + ". Michelle:"
                answer, start_prompt = GPTPlatform.conversationWithVirtualAssistant(start_prompt, name)

                window['-OUTPUT-'].update("YOU: " + text + "\n" + "MICHELLE: " + answer)
                window['-CONVO-'].update("")

                with open("conversation_history/conversation_with_michelle_4.txt", 'w') as f:
                    f.write(start_prompt)

            elif event == 'Return:36': #return:36 is the Enter button
                start_prompt += ". " + name + ": " + str(text) + ". Michelle:"
                answer, start_prompt = GPTPlatform.conversationWithVirtualAssistant(start_prompt, name)

                window['-OUTPUT-'].update("YOU: " + text + "\n" + "MICHELLE: " + answer)
                window['-CONVO-'].update("")

                with open("conversation_history/conversation_with_michelle_4.txt", 'w') as f: # add date & time for better logging of convo history
                    f.write(start_prompt)

    except Exception as e:
        print(e)
        print("Conversation ended.")


if __name__ == '__main__':
    TextToSpeech.textToSpeechAudio("Hey hey! Before we start, I'd like to ask you to answer the following questions for the best experience.")
    filename = 'audio/clean_audio.wav'
    playsound(filename)
    os.remove(filename)
    name = input("Enter your name: ")
    gender = input("Enter your gender (man, woman): ")
    skin_type = input("Enter your skin type (dry or sensitive): ")
    hair_type = input("Enter your hair type (dry or normal): ")
    main_app(name, gender, skin_type, hair_type)