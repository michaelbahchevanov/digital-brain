import openai
import os
from playsound import playsound
from .text_to_speech import TextToSpeech
import configparser


# Method to get the api key of OpenAI
def get_api_key():
    config = configparser.ConfigParser()
    config.read('helpers/openai/openai_config.ini')
    return config['openai']['api']


class GPTPlatform:
    openai.api_key = get_api_key()

    # Method to do intent classification
    def intentClassifier(sentence):
        response = openai.Completion.create(
            engine="davinci",
            prompt="The following are the intents that the model is able to classify: GetCurrentDate, Weather, "
                   "RemoveFromCart, AddToCart, SearchCart. "
                   "Text: Add this product to my shopping cart."
                   "Intent: AddToCart"
                   "Text: Remove the jeans from my cart."
                   "Intent: RemoveFromCart"
                   "Text: I want a black one."
                   "Intent: ConverseWithAI"
                   "Text: Where can I find clothes for kids?"
                   "Intent: SearchStore"
                   "Text: These jeans look great on me! I really like it"
                   "Intent: ConverseWithAI"
                   "Text: I like the design of this t-shirt, what do you think of it?"
                   "Intent: ConverseWithAI"
                   "Text: Hello"
                   "Intent: ConverseWithAI"
                   "Text: Search for the cheapest shoes in the store."
                   "Intent: SearchStore"
                   "Text: What is the most expensive item in my shopping cart?"
                   "Intent: SearchCart"
                   "Text: " + sentence +
                   "Intent:",
            temperature=0,
            max_tokens=15,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["Text:", "Intent:"]
        )

        return response['choices'][0]['text']

    # Method for a conversation with a virtual assistant (with context of a in-store virtual assistant)
    def conversationWithVirtualAssistant(converse, name):

        response = openai.Completion.create(
            engine="davinci-instruct-beta-v3",
            prompt=converse,
            temperature=0.4,
            max_tokens=100,
            top_p=1,
            frequency_penalty=2,
            presence_penalty=2,
            stop=["\n", " Michelle:", name+":"]
        )

        text_response = response['choices'][0]['text']

        # TextToSpeech.textToSpeechAudio(text_response)
        # filename = 'audio/clean_audio.wav'
        # playsound(filename)
        # os.remove(filename)

        new_prompt = converse + text_response

        return text_response, new_prompt

