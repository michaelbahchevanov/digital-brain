# Load the libraries that are needed
import os
import torch
import time
import openai
import speech_recognition as sr
import soundfile as sf

from playsound import playsound
from TTS.utils.generic_utils import setup_model
from TTS.utils.io import load_config
from TTS.utils.text.symbols import symbols, phonemes
from TTS.utils.audio import AudioProcessor
from TTS.utils.synthesis import synthesis
from TTS.vocoder.utils.generic_utils import setup_generator

# Define api key and cuda
openai.api_key = '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'
use_cuda = False


# Paths to models and configs
TTS_MODEL = "tts_model.pth.tar"
TTS_CONFIG = "config.json"
VOCODER_MODEL = "vocoder_model.pth.tar"
VOCODER_CONFIG = "config_vocoder.json"


# Load configuration files
TTS_CONFIG = load_config(TTS_CONFIG)
VOCODER_CONFIG = load_config(VOCODER_CONFIG)


# load the audio processor
ap = AudioProcessor(**TTS_CONFIG.audio)


# Define speakers
speaker_id = None
speakers = []


# Define model
num_chars = len(phonemes) if TTS_CONFIG.use_phonemes else len(symbols)
model = setup_model(num_chars, len(speakers), TTS_CONFIG)


# Load model state with torch.load()
cp = torch.load(TTS_MODEL, map_location=torch.device('cpu'))


# load the model
model.load_state_dict(cp['model'])
if use_cuda:
    model.cuda()
model.eval()


# set model stepsize
if 'r' in cp:
    model.decoder.set_r(cp['r'])


# Load vocoder model
vocoder_model = setup_generator(VOCODER_CONFIG)
vocoder_model.load_state_dict(torch.load(VOCODER_MODEL, map_location="cpu")["model"])
vocoder_model.remove_weight_norm()
vocoder_model.inference_padding = 0


ap_vocoder = AudioProcessor(**VOCODER_CONFIG['audio'])
if use_cuda:
    vocoder_model.cuda()
vocoder_model.eval()


###
### Method that sends API requests to GPT-3 Completion API with a defined prompt.
###
def gptConversationalModel(convo):
    global txt
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
        gptContextModel(convo)
    else:
        print("Michelle Green: " + response['choices'][0]['text'])
        textToSpeechAudio(response['choices'][0]['text'])
        filename = '../clean_audio.wav'
        playsound(filename)
        os.remove(filename)
        txt = "Michelle Green: " + response['choices'][0]['text']


###
### Method that sends API requests to GPT-3 Answering API with a JSONL document ID as the file to use
###
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

    textToSpeechAudio(provided_answer['answers'][0])
    filename = '../clean_audio.wav'
    playsound(filename)
    os.remove(filename)


###
### Method that converts the audio array to wav file and saves the file as clean_audio.wav
###
def textToSpeechAudio(input_text):
    align, spec, stop_tokens, wav = tts(model, input_text, TTS_CONFIG, use_cuda, ap, use_gl=False, figures=True)
    sf.write('../clean_audio.wav', wav, 22050, "PCM_16")


###
### Method that build the text to speech syntesizer
###
def tts(model, text, CONFIG, use_cuda, ap, use_gl, figures=True):
    t_1 = time.time()
    waveform, alignment, mel_spec, mel_postnet_spec, stop_tokens, inputs = synthesis(model, text, CONFIG, use_cuda, ap, speaker_id, style_wav=None, truncated=False, enable_eos_bos_chars=CONFIG.enable_eos_bos_chars)

    if not use_gl:
        waveform = vocoder_model.inference(torch.FloatTensor(mel_postnet_spec.T).unsqueeze(0))
        waveform = waveform.flatten()
    if use_cuda:
        waveform = waveform.cpu()
    waveform = waveform.numpy()
    return alignment, mel_postnet_spec, stop_tokens, waveform


###
### Method that runs the application
### Using SpeechRecognition library inside the function to perform speech to text using Google's speech to text API
###
def main_app():
    r = sr.Recognizer()

    try:
        while True:
            with sr.Microphone() as source:
                print("Please wait 1 second before speaking!")
                r.adjust_for_ambient_noise(source, duration=1)  # reduce noise
                audio_text = r.listen(source, timeout=4)
                print("Time over, thanks")
                text = r.recognize_google(audio_text)
                print("You: " + text)
                gptConversationalModel(text)

                if source is None:
                    continue
    except Exception as e:
        print(e)
        print("Conversation ended.")

###
### Application
###
if __name__ == '__main__':
    response = input("\nStart conversation (Yes or No)? ")

    if response[0] == "y":
        main_app()
    elif response[0] == "n":
        print("Good bye")