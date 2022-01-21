import sys
import torch
import soundfile as sf

sys.path.append('TTS')
from TTS.tts.utils.generic_utils import setup_model
from TTS.utils.io import load_config
from TTS.tts.utils.text.symbols import symbols, phonemes, make_symbols
from TTS.utils.audio import AudioProcessor
from TTS.tts.utils.synthesis import synthesis
from TTS.vocoder.utils.generic_utils import setup_generator
from TTS.tts.utils.io import load_checkpoint


class TextToSpeech:
    # Colab: https://colab.research.google.com/drive/1uV2CD1hWx5FGUrcIQjdZfI717AMj8-kP?usp=sharing
    # Source: https://github.com/mozilla/TTS

    use_cuda = False

    # model paths
    TTS_MODEL = "helpers/text_to_speech/tts_model.pth.tar"
    TTS_CONFIG = "helpers/text_to_speech/config.json"
    VOCODER_MODEL = "helpers/text_to_speech/vocoder_model.pth.tar"
    VOCODER_CONFIG = "helpers/text_to_speech/config_vocoder.json"

    # load configs
    TTS_CONFIG = load_config(TTS_CONFIG)
    VOCODER_CONFIG = load_config(VOCODER_CONFIG)
    TTS_CONFIG.audio['stats_path'] = "helpers/text_to_speech/scale_stats.npy"
    VOCODER_CONFIG.audio['stats_path'] = "helpers/text_to_speech/scale_stats_vocoder.npy"

    # load the audio processor
    ap = AudioProcessor(**TTS_CONFIG.audio)

    # multi speaker
    speakers = []
    speaker_id = None

    if 'characters' in TTS_CONFIG.keys():
        symbols, phonemes = make_symbols(**TTS_CONFIG.characters)

    # load the model
    num_chars = len(phonemes) if TTS_CONFIG.use_phonemes else len(symbols)
    model = setup_model(num_chars, len(speakers), TTS_CONFIG)

    # load model state
    model, _ =  load_checkpoint(model, TTS_MODEL, use_cuda=use_cuda)
    model.eval()

    # LOAD VOCODER MODEL
    vocoder_model = setup_generator(VOCODER_CONFIG)
    vocoder_model.load_state_dict(torch.load(VOCODER_MODEL, map_location="cpu")["model"])
    vocoder_model.remove_weight_norm()
    vocoder_model.inference_padding = 0

    # scale factor for sampling rate difference
    scale_factor = [1,  VOCODER_CONFIG['audio']['sample_rate'] / ap.sample_rate]

    ap_vocoder = AudioProcessor(**VOCODER_CONFIG['audio'])
    if use_cuda:
        vocoder_model.cuda()
    vocoder_model.eval()

    def interpolate_vocoder_input(scale_factor, spec):
        """Interpolation to tolarate the sampling rate difference
        btw tts model and vocoder"""
        spec = torch.tensor(spec).unsqueeze(0).unsqueeze(0)
        spec = torch.nn.functional.interpolate(spec, scale_factor=scale_factor, mode='bilinear').squeeze(0)
        return spec


    def tts(model, text, CONFIG, use_cuda, ap, use_gl, figures=True):
        # run tts
        waveform, alignment, mel_spec, mel_postnet_spec, stop_tokens, inputs =\
        synthesis(model,
                   text,
                   CONFIG,
                   use_cuda,
                   ap,
                   TextToSpeech.speaker_id,
                   None,
                   False,
                   CONFIG.enable_eos_bos_chars,
                   use_gl)
        # run vocoder
        mel_postnet_spec = ap._denormalize(mel_postnet_spec.T).T
        if not use_gl:
            vocoder_input = TextToSpeech.ap_vocoder._normalize(mel_postnet_spec.T)
            if TextToSpeech.scale_factor[1] != 1:
                vocoder_input = TextToSpeech.interpolate_vocoder_input(TextToSpeech.scale_factor, vocoder_input)
            else:
                vocoder_input = torch.tensor(vocoder_input).unsqueeze(0)
            waveform = TextToSpeech.vocoder_model.inference(vocoder_input)
        # format output
        if use_cuda and not use_gl:
            waveform = waveform.cpu()
        if not use_gl:
            waveform = waveform.numpy()
        waveform = waveform.squeeze()

        return alignment, mel_postnet_spec, stop_tokens, waveform

    # Method to convert audio array to wav file and save the file for later use
    def textToSpeechAudio(input_text):
        align, spec, stop_tokens, wav = TextToSpeech.tts(TextToSpeech.model, input_text, TextToSpeech.TTS_CONFIG, TextToSpeech.use_cuda, TextToSpeech.ap, use_gl=False, figures=True)
        sf.write('audio/clean_audio.wav', wav, 22050, "PCM_16")