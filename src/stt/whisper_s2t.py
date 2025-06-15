import whisper
import os

class S2T_Whisper:
    """Speech-to-text model based on Whisper """
    MODELS = "tiny", "base", "small", "medium", "large-v1", "large-v2"
    # https://github.com/openai/whisper
    def __init__(self, model_selected: str ="base"):
        """
        Initialize the speech-to-text model.

        Args:
            model_selected (str): whisper model, must be one of the following: "tiny", "base", "small", "medium", "large-v1", "large-v2".
        """
        self.model: whisper.Whisper = whisper.load_model(model_selected)

    def get_text(self, source_audio: str, language: str, show_all: bool=False):
        """
        Execute the speech-to-text transcription on the audio.
        
        Args:
            source_audio (str): a valid path to an audio file.
            language (str): source_audio language, for correct recognition, in iso_code_2.
            show_all (bool): if True, all the detais of the transcription will be returned. If False, only the text will be returned.
        """                
        try:
            transcription = self.model.transcribe(
                        audio=source_audio,
                        language=language,
                        task='transcribe',
                        fp16=False
                        # temperature=temperature,
                        # compression_ratio_threshold=compression_ratio_threshold,
                        # logprob_threshold=logprob_threshold,
                        # no_speech_threshold=no_speech_threshold,
                        # condition_on_previous_text=condition_on_previous_text,
                        # initial_prompt=initial_prompt,
                        # **whisper_extra_args,
                    )            
        except Exception as e:
            print(f"Error in whisper: {e}")
            return None
        if show_all:
            return transcription
        else:
            return transcription['text']

    def supported_languages(self, as_dict: bool=False):
        """
        Show the supported_languages for the current model.

        Args:
            as_dict (bool): if True, the result is a dictionary with the languages and the codes. If False, the result is a list with the codes.
        """
        iso_code_2 = {"Bulgarian":"bg",
                    "Catalan":"ca",
                    "Croatian": "hr",
                    "Czech": "cs",
                    "Danish": "da",
                    "Dutch":"nl",
                    "English":"en",
                    "Estonian": "et",
                    "Finnish":"fi",
                    "French":"fr",
                    "German":"de",
                    "Greek":"el",
                    "Hungarian":"hu", 
                    "Irish": "ga",
                    "Italian":"it",
                    "Latvian":"lv",
                    "Lithuanian":"lt",
                    "Maltese":"mt",
                    "Polish":"pl",
                    "Portuguese":"pt",
                    "Romanian":"ro", 
                    "Slovak":"sk",
                    "Slovene":"sl",
                    "Spanish":"es",
                    "Swedish":"sv"}
        if as_dict:
            return iso_code_2
        else:
            return list(iso_code_2.values())
