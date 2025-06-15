import os
import gc
import shutil
import warnings
import json
import re
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
import torchaudio
from dotenv import load_dotenv
import stt.whisper_s2t as whisper_s2t
import audio_process.audiowork as audiowork
import summarize.llm as llm
from audacity import create_audacity_project_edited
from settings import *

transcription_result_file = os.path.join(FINISHED_DIR, "result.txt")

load_dotenv()
warnings.filterwarnings("ignore", category=FutureWarning)
def main(audio_path, language='es'):
    # Check if the path is valid
    if not os.path.isfile(audio_path):
        print(f"\n Audio file not found: {audio_path}")
        return
    print(f"\n Using audio file: {audio_path}:\n")
    
    audio_adjustments(audio_path)
    simple_transcription(audio_path, language)
    summarize("", audio_path)

def audio_adjustments(audio_path):
    waveform, sample_rate = torchaudio.load(audio_path)
    destination_file = os.path.join(IN_PROCESS_DIR, f"ready_{os.path.splitext(os.path.basename(audio_path))[0]}.wav")

    # checking if the audio has the right format, and if not fix it
    if sample_rate != 16000 or waveform.shape[0] > 1:
        audiowork.adjust_audio(audio_path, destination_file)
    else:      
        shutil.copy(audio_path, destination_file)
    return destination_file

def simple_transcription(right_format_file, language='es', whisper_model="small"):
    model = whisper_s2t.S2T_Whisper(whisper_model) # "medium", "small", "base", "tiny"

    text = model.get_text(right_format_file, language, True)
    with open(transcription_result_file, 'w+', encoding="utf-8") as file:
        for item in text["segments"]:
            file.write(f'(From {round(item["start"], 2)} to {round(item["end"], 2)}): {item["text"]} \n')
    del model
    gc.collect()

def summarize(audio_context_info, audio_path):
    # summarize 
    with open(transcription_result_file, 'r', encoding="utf-8") as file:
        transcription_file_content = file.read().split('\n')

    summary_dicts = llm.summarize_transcription(transcription_file_content, audio_context_info, lines_per_chunk=40)
    output_json = os.path.join(FINISHED_DIR, f"summary_result_{os.path.splitext(os.path.basename(audio_path))[0]}.json")
    with open(output_json, 'w+') as file:
        json.dump(summary_dicts, file, indent=2)
    return output_json

# Parse chunk string into structured data
def parse_chunk(chunk_str):
    match = re.match(r'\(From ([\d.]+) to ([\d.]+)\): (.+)', chunk_str)
    if match:
        return {
            "start": float(match.group(1)),
            "end": float(match.group(2)),
            "text": match.group(3)
        }
    return None

def get_path():
    done = False
    while not done:
        user_input = input("\nWrite the path to the file:\n")
        
        if not os.path.isfile(user_input):
            print(f"\n Audio file not found: {user_input}")
            if input("Do you want to try again? Y/N\n")== "Y":
                continue
            else:
                break
        done = True
        
    if done:
        return user_input
        
    return False

if __name__ == "__main__":
    path = get_path()

    if path != False:
        main(path)

