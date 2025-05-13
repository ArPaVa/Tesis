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
    if not os.path.isfile(audio_path):
        print(f"\n Audio file not found: {audio_path}")
    print(f"\n Using audio file: {audio_path}:\n")
    
    waveform, sample_rate = torchaudio.load(audio_path)

    if sample_rate != 16000 or waveform.shape[0] > 1:
        audiowork.pyannotefix(audio_path)
    else:
        # Specify the destination folder path
        destination_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"in_process",f"ptnready_{os.path.basename(audio_path)}")
        
        # Copy the file to the destination folder
        shutil.copy(audio_path, destination_file)
    pyannote_working_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"in_process",f"ptnready_{os.path.splitext(os.path.basename(audio_path))[0]}.wav")
    model = whisper_s2t.S2T_Whisper("medium") # recommended # 138 MB
    # model = whisper_s2t.S2T_Whisper("tiny")  # 73 MB

    api_key = os.getenv("HF_ACCESS_TOKEN")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",use_auth_token=api_key)
    with ProgressHook() as hook:
        diarization = pipeline(pyannote_working_file, hook=hook)
    
    rttm_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)),"in_process",f"ptnready_{os.path.splitext(os.path.basename(audio_path))[0]}.rttm")
    with open(rttm_directory, "w") as rttm:
        diarization.write_rttm(rttm)
    audiowork.rttm_join_speakers(rttm_directory)

    rttm_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)),"in_process",f"merged_ptnready_{os.path.splitext(os.path.basename(audio_path))[0]}.rttm")
    result = audiowork.parse_rttm(rttm_directory)
    for line_num, info in result.items():
        print(f"Line {line_num}: {info}")
    
    end_file_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)),"finished",f"{os.path.splitext(os.path.basename(audio_path))[0]}.txt")
    r = audiowork.process_audio_segments(result,pyannote_working_file, model, language, end_file_directory )
    # #text = model.get_text(audio_path, language,True)
    # #for item in text["segments"]:
    # #    print(f'{item["text"]} \n from {item["start"]} to {item["end"]}') 
    # #    #print(f'{item["text"]}')
    # #print(text)
    # #print(len(text["segments"]))
    # #print(audio_path)
    # base_name = os.path.basename(audio_path)
    # #print(base_name)
    # file_name_without_extension = os.path.splitext(base_name)[0]
    # #print(file_name_without_extension)  # Output: file
    # with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "in_process",file_name_without_extension+".json"),"w") as json_file:
    #     json.dump(text,json_file)
   
    # return text 
 
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
#"C:\Users\ArPaVa\Pictures\Screenshots\audio_2024-11-20_09-24-37.ogg"
#"C:/Users/ArPaVa/Documents/VS Code/Tesis/Code/Tesis/test.wav"
load_dotenv()
path = get_path()
if path != False:
    main(path)