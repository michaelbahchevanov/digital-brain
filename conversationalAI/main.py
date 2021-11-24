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
def main_app():
    topics = ['intent', 'sentiment', 'conversation']
    print(topics)

    TextToSpeech.textToSpeechAudio("Choose a demo. Intent or Sentiment Classification, or just a conversation with a virtual assistant. After choosing, speak when you hear the ding!")
    filename = 'audio/clean_audio.wav'
    playsound(filename)

    start_prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. Human: Hello, who are you? AI: I am an AI created by OpenAI. How can I help you today? Human: neutral. AddToCart. Add this item to my shopping cart.  AI: Okay, the item has been added to your shopping cart. Human: negative. ConverseWithAI. I don't like how this jacket looks on me. AI: Is there a reason why you don't like the jacket? Human: neutral. RemoveFromCart. Yes, there's a reason, the jacket is too short, please remove the jacket from the cart. AI: The jacket has been removed from the shopping cart.  Human: neutral. SearchCart. Search for jeans with the color black in my shopping cart. AI: Here's a list of all the black jeans in your shopping cart. Human: positive. ConverseWithAI. These jeans look great on me! I really like it. AI: It fits you so well. Would you like me to add these jeans to your shopping cart? Human: neutral. AddToCart. Yes, add the jeans to my shopping cart. AI: Okay, I have added the jeans to your shopping cart. Human: neutral. Weather. What is the weather forecast for tomorrow? AI: Tomorrow is going to be sunny with a high of 21 degrees. AI: Is there anything else I can do for you? Human: Yes. AI: Okay, what would you like me to do? Human: positive. ConverseWithAI. I like the design of this t-shirt, what do you think of it? AI: I like the design of this t-shirt too. What color do you want? Human: neutral. ConverseWithAI. I want a black one. AI: Okay, I will get you one in black. Human: neutral. AddToCart. Can you add it to my cart? AI: Okay, I have added the t-shirt to your shopping cart. Human: negative. ConverseWithAI. It annoys me when there's no one around to help me. AI: I can help you. Please go ahead. Human: neutral. SearchStore. Search for the cheapest shoes in the store. AI: Okay, here's a list of the cheapest shoes in the store. Human: neutral. AddToCart. Pick the cheapest shoes from the list and add it to my shopping cart. AI: Okay, I have added the shoes to your shopping cart"

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
                text = SpeechToText.speechToText("start")
                if text == 'stop':
                    return False
                else:
                    start_prompt += ". Human: " + SentimentClassifier.get_sentiment(text) + "." + GPTPlatform.intentClassifier(text) + ". " + str(text) + ". AI:"
                    answer, start_prompt = GPTPlatform.conversationWithVirtualAssistant(start_prompt)
                    print("start prompt: " + start_prompt)
    except Exception as e:
        print(e)
        print("Conversation ended.")


if __name__ == '__main__':
    run_conversational_tasks([
        start_cv(),
        main_app(),
    ])
