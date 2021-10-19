import os
import openai

from playsound import playsound
from conversationalAI.models.text_to_speech import TextToSpeech


class QuestionAnswering:
    # Method to get answers based on context via openai GPT-3 Answer API
    def gptContextModel(question):
        provided_answer = openai.Answer.create(
            search_model="ada",
            model="curie-instruct-beta",
            question=question,
            file="file-tqK7GAt4ZkOpJi9HdCw2070P",
            examples_context="In 2017, U.S. life expectancy was 78.6 years.",
            examples=[["What is human life expectancy in the United States?",
                       "The life expectancy in the United States is 78 years."]],
            max_rerank=5,
            max_tokens=1000,
            stop=["\n"]
        )

        TextToSpeech.textToSpeechAudio(provided_answer['answers'][0])
        # textToSpeechAudio(provided_answer['answers'][0])
        filename = '../clean_audio.wav'
        playsound(filename)
        os.remove(filename)