import sys
import torch
import time
import soundfile as sf
import os

sys.path.append('TTS')
from TTS.utils.generic_utils import setup_model
from TTS.utils.io import load_config
from TTS.utils.text.symbols import symbols, phonemes
from TTS.utils.audio import AudioProcessor
from TTS.utils.synthesis import synthesis
from TTS.vocoder.utils.generic_utils import setup_generator


class TextToSpeech:
    use_cuda = False

    # model paths
    TTS_MODEL = os.getcwd() + "/helpers/tts_model.pth.tar"
    TTS_CONFIG = "helpers/config.json"
    VOCODER_MODEL = "helpers/vocoder_model.pth.tar"
    VOCODER_CONFIG = "helpers/config_vocoder.json"

    # load configuration files
    TTS_CONFIG = load_config(TTS_CONFIG)
    VOCODER_CONFIG = load_config(VOCODER_CONFIG)

    # load the audio processor
    ap = AudioProcessor(**TTS_CONFIG.audio)

    # multi speaker
    speaker_id = None
    speakers = []

    # load the model
    num_chars = len(phonemes) if TTS_CONFIG.use_phonemes else len(symbols)
    model = setup_model(num_chars, len(speakers), TTS_CONFIG)

    # load model state
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

    # model.length_scale = 0.8  # set speed of the speech.
    # model.noise_scale = 0.01  # set speech variation

    # Method to generate text to speech synthesis
    def tts(model, text, CONFIG, use_cuda, ap, use_gl, figures=True):
        t_1 = time.time()
        waveform, alignment, mel_spec, mel_postnet_spec, stop_tokens, inputs = synthesis(model, text, CONFIG, use_cuda, ap, TextToSpeech.speaker_id, style_wav=None, truncated=False, enable_eos_bos_chars=CONFIG.enable_eos_bos_chars)

        if not use_gl:
            waveform = TextToSpeech.vocoder_model.inference(torch.FloatTensor(mel_postnet_spec.T).unsqueeze(0))
            waveform = waveform.flatten()
        if use_cuda:
            waveform = waveform.cpu()
        waveform = waveform.numpy()
        return alignment, mel_postnet_spec, stop_tokens, waveform

    # Method to convert audio array to wav file and save the file for later usage
    def textToSpeechAudio(input_text):
        align, spec, stop_tokens, wav = TextToSpeech.tts(TextToSpeech.model, input_text, TextToSpeech.TTS_CONFIG, TextToSpeech.use_cuda, TextToSpeech.ap, use_gl=False, figures=True)
        sf.write('../clean_audio.wav', wav, 22050, "PCM_16")
