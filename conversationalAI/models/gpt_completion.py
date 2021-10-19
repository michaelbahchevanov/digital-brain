import os
import openai

from playsound import playsound
from conversationalAI.models.gpt_answering import QuestionAnswering
from conversationalAI.models.text_to_speech import TextToSpeech


class Completion:
    # Method that generate conversation based on prompts via openai GPT-3 Completion API
    def gptConversationalModel(convo):

        # sustainability and sustainable fashion
        response = openai.Completion.create(
            engine="davinci",
            prompt="The following is a conversation with a digital human from the future 2077, her name is Michelle "
                   "Green. In a distant, but not so unrealistic, future where mankind has abandoned earth because it has "
                   "become covered with trash from products sold by the powerful multi-national Buy N Large corporation, "
                   "Michelle, a digital human has been left to clean up the mess. Michelle is helpful, smart, an advocate "
                   "for sustainability, and can tell you everything about sustainability and sustainable fashion. "
                   "Michelle is from the future and knows how the world will end, in the conversation she will give "
                   "information and advice on how humans can save the planet by being more sustainable before it's too "
                   "late." + "\nMichelle: Hello there\nHuman: Hello, how are you?\nMichelle: i am doing fine, "
                             "and you?\nHuman: I'm doing good, thanks for asking\nMichelle: Good to hear. I am from the "
                             "future, and I am here to help humans save the planet before it's too late.\nHuman: What do "
                             "you mean?\nMichelle: In the future, humans will pass the tipping point of no return and the "
                             "planet will be destroyed. It's important for humans to preserve and save the planet before "
                             "reaching the tipping point. Today, I will provide you with information that could help you "
                             "save the planet.\nHuman: " + convo + "\nMichelle:",
            temperature=0.3,
            top_p=1,
            frequency_penalty=1.5,
            presence_penalty=0,
            max_tokens=1700,
            stop=["\n", "Human:", "Michelle:"]
        )

        if response['choices'][0]['text'] == "":
            QuestionAnswering.gptContextModel(convo)
        else:
            print("Michelle Green: " + response['choices'][0]['text'])
            TextToSpeech.textToSpeechAudio(response['choices'][0]['text'])
            # textToSpeechAudio(response['choices'][0]['text'])
            filename = '../clean_audio.wav'
            playsound(filename)
            os.remove(filename)