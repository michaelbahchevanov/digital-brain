import openai
import os
from playsound import playsound

from .text_to_speech import TextToSpeech
import configparser


def get_api_key():
    config = configparser.ConfigParser()
    config.read('helpers/config.ini')
    return config['openai']['api']


class GPTPlatform:
    openai.api_key = get_api_key()

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

        whitespaced_response = response['choices'][0]['text']

        if whitespaced_response[-1].isspace():
            newstring = whitespaced_response[:-1]+'.'

        if response['choices'][0]['text'] == "":
            GPTPlatform.gptContextModel(convo)
        else:
            print("Michelle Green:" + newstring)
            TextToSpeech.textToSpeechAudio(newstring)
            filename = 'audio/clean_audio.wav'
            playsound(filename)
            os.remove(filename)

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
        filename = '../clean_audio.wav'
        playsound(filename)
        os.remove(filename)

    def brandDetecion(brand):
        response = openai.Completion.create(
            engine="davinci",
            prompt="Sustainability is based on a simple principle: Everything that we need for our survival and "
                   "well-being depends, either directly or indirectly, on our natural environment. To pursue "
                   "sustainability is to create and maintain the conditions under which humans and nature can exist in "
                   "productive harmony to support present and future generations.\n\nSustainability is Nike's belief that "
                   "we can deliver long-term growth and profit while improving the environment. Sustainability is a "
                   "fundamental part of Nike's business model to drive a more profitable, lower-carbon way of doing "
                   "business.\n\nWe believe the world needs a new model for business. Our mission is to provide consumers "
                   "around the world with products that enrich their lives and bring them closer to the athletes they "
                   "love while striving to minimize the impact on our planet.\n\nSustainability is Ben & Jerry's "
                   "commitment to source 100% of its electricity from renewable energy by 2020. To learn more about our "
                   "environmental initiatives, please visit benjerry.com/sustainable-initiatives.\n\nSustainability is a "
                   "core value at The Body Shop and it is at the heart of everything we do. We have been working for 30 "
                   "years to source ingredients from suppliers who share our commitment to sustainable development and "
                   "environmental protection, and we have been campaigning on issues such as fair trade, rainforest "
                   "protection, animal testing, and global warming since the beginning of the company. We are committed "
                   "to building a business that lasts by embedding sustainability into everything we do – from the way we "
                   "source ingredients to how we run our business.\n\nSustainability is Apple's commitment to leave the "
                   "world better than we found it. We are committed to leaving the world better than we found it. We "
                   "believe in the power of human ingenuity to solve problems and create a better future for people "
                   "everywhere. We believe in leaving the world better than we found it.\n\nSustainability is Adidas's "
                   "commitment to the environment and to the communities in which we operate. We are committed to "
                   "creating products that are better for the environment and better for people. We believe that we can "
                   "make a positive difference by minimizing our environmental footprint, respecting human rights, "
                   "and empowering communities.\n\nSustainability is" + brand + "'s",
            temperature=0.8,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.8,
            presence_penalty=0,
            stop=["\n"]
        )

        whitespaced_response = response['choices'][0]['text']

        if whitespaced_response[-1].isspace():
            newstring = whitespaced_response[:-1]+'.'

        print("Michelle Green:" + newstring)
        TextToSpeech.textToSpeechAudio(newstring)
        filename = 'audio/clean_audio.wav'
        playsound(filename)
        os.remove(filename)


    def brandDetectionUsingSentiment(sentiment):
        response = openai.Completion.create(
          engine="davinci",
          prompt="The following is a conversation with an AI assistant, her name is Michelle Green. Michelle has a lot of knowledge about every brand "
                 "in the world and their efforts on sustainability. Michelle is wise, clever, creative and her information about brands are based on facts only. If the sentiment that the assistant will get via "
                 "an API is positive, the assistant will say something positive about that brand and its efforts on "
                 "sustainability. If the sentiment is negative, the assistant will ask you why do you think that and "
                 "proceed to say "
                 "something positive about the brand. If the sentiment is neutral the assistant will say something "
                 "positive about that brand and its efforts on sustainability. SENTIMENT: negative. I don't "
                 "believe Nike is doing enough to help save the planet. AI: But the brand uses recycled materials in "
                 "its products. They are also making efforts to reduce energy consumption with their product design "
                 "and manufacturing process. SENTIMENT: positive. I like that Apple is making efforts to continually "
                 "improve the environment. AI: That is a very smart move. Just last year, Apple invested $4 billion "
                 "in renewable energy and claims to be the largest corporate buyer of green power in the "
                 "world. SENTIMENT: negative. I don't believe Patagonia cares about the planet. AI: You are "
                 "incorrect. Patagonia is committed to conservation and environmental activism. The company has "
                 "donated millions of dollars to organizations like the Waterkeeper Alliance, which is dedicated to "
                 "protecting waterways throughout the world. SENTIMENT: neutral. Do you think that scotch & soda "
                 "cares about saving the planet? AI: Scotch & soda is an apparel brand that sells clothing produced "
                 "ethically and sustainably. SENTIMENT: neutral. I think that Microsoft is really making efforts to "
                 "make the world a better place. AI: I am glad you recognize Microsoft for their efforts in "
                 "sustainability. The company is committed to achieving net-zero cloud emissions by 2012, which means "
                 "it will use clean energy sources to offset its environmental impact on the planet. SENTIMENT: "
                 "negative. I hate that calvin klein only care about money and is not helping to save the animals "
                 "they butcher to make clothes with. AI: Calvin Klein is committed to protecting animals and the "
                 "natural resources they inhabit. SENTIMENT: " + sentiment + " AI:",
          temperature=0.5,
          max_tokens=1000,
          top_p=1,
          frequency_penalty=1.5,
          presence_penalty=0.8,
          stop=["AI:", "SENTIMENT:"]
        )

        whitespaced_response = response['choices'][0]['text']

        if whitespaced_response[-1].isspace():
            newstring = whitespaced_response[:-1]+'.'

        print("Michelle Green:" + newstring)
        TextToSpeech.textToSpeechAudio(newstring)
        filename = 'audio/clean_audio.wav'
        playsound(filename)
        os.remove(filename)