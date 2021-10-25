import os
import openai

from playsound import playsound
from .gpt_answering import QuestionAnswering
from .text_to_speech import TextToSpeech


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
                   "late." + "Michelle:Hey there Human:Hello, how are you? Michelle:I am good, "
                             "and you? Human:I'm doing good, thanks for asking Michelle:Good to hear. I am from the "
                             "future, and I am here to help humans save the planet before it's too late. Human: What do "
                             "you mean? Michelle:In the future, humans will pass the tipping point of no return and the "
                             "planet will be destroyed. It's important for humans to preserve and save the planet before "
                             "reaching the tipping point. Today, I will provide you with information that could help you "
                             "save the planet. Human:" + convo + " Michelle:",
            temperature=0.6,
            top_p=1,
            frequency_penalty=1.5,
            presence_penalty=0,
            max_tokens=1700,
            stop=["Human:", "Michelle:"]
        )

        # res = response['choices'][0]['text']
        # last_char = res[-1]
        # print("starting"+last_char+res)
        # if last_char.isspace():
        #     print("whitespace" + last_char + "here")
        # for i in range(len(res)):
        #     if res[i].isspace():
        #         print(i)

        if response['choices'][0]['text'] == "":
            QuestionAnswering.gptContextModel(convo)
        else:
            print("Michelle Green:" + response['choices'][0]['text'][:-1])
            TextToSpeech.textToSpeechAudio(response['choices'][0]['text'][:-1])
            filename = '../clean_audio.wav'
            playsound(filename)
            os.remove(filename)
