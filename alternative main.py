import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"stt"))
import whisper_s2t
import warnings
import json
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
import torchaudio
from dotenv import load_dotenv
import audiowork
import shutil
#from .stt import whisper_s2t

warnings.filterwarnings("ignore", category=FutureWarning)
def main(audio_path, language='es'):
    # Check if the path is valid
    if not os.path.isfile(audio_path):
        print(f"\n Audio file not found: {audio_path}")
    print(f"\n Using audio file: {audio_path}:\n")
    
    waveform, sample_rate = torchaudio.load(audio_path)
    #checking if the audio has the right format, and if not fix it
    if sample_rate != 16000 or waveform.shape[0] > 1:
        audiowork.pyannotefix(audio_path)
    else:      
        destination_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"in_process",f"ptnready_{os.path.basename(audio_path)}")
        shutil.copy(audio_path, destination_file)
    
    pyannote_working_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"in_process",f"ptnready_{os.path.splitext(os.path.basename(audio_path))[0]}.wav")
    model = whisper_s2t.S2T_Whisper("medium") # recommended # 138 MB
    # model = whisper_s2t.S2T_Whisper("tiny")  # 73 MB

    text = model.get_text(pyannote_working_file, language,True)
    with open("alternative_main_result.txt", 'w', encoding="utf-8") as file:
        for item in text["segments"]:
            file.write(f'(From {round(item["start"],2)} to {round(item["end"],2)}): {item["text"]} \n')
            #print(f'{item["text"]} \n from {item["start"]} to {item["end"]}') 
            #print(f'{item["text"]}')
        #print(text)
        #print(len(text["segments"]))
        #print(audio_path)
        #base_name = os.path.basename(audio_path)
        #print(base_name)
        #file_name_without_extension = os.path.splitext(base_name)[0]
        #print(file_name_without_extension)  # Output: file
        #with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "in_process",file_name_without_extension+".json"),"w") as json_file:
        #    json.dump(text,json_file)

 
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

load_dotenv()
path = get_path()
if path != False:
    main(path)