import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"stt"))
import whisper_s2t
import warnings
#from .stt import whisper_s2t

warnings.filterwarnings("ignore", category=FutureWarning)
def main(audio_path, language='es'):
    model = whisper_s2t.S2T_Whisper("base") # recommended # 138 MB
    # model = whisper_s2t.S2T_Whisper("tiny")  # 73 MB
    if not os.path.isfile(audio_path):
        print(f"\n Audio file not found: {audio_path}")
    print(f"\n Using audio file: {audio_path}:\n")
       
    text = model.get_text(audio_path, language)
    print(text)
    return text

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
#C:\Users\ArPaVa\Pictures\Screenshots\audio_2024-11-20_09-24-37.ogg
#"C:/Users/ArPaVa/Documents/VS Code/Tesis/Code/FirstSteps/test.wav"

path = get_path()
if path != False:
    main(path)