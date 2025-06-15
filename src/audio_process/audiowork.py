import os
from pydub import AudioSegment
import pandas as pd
import json
from settings import *

def get_audio_duration(audio_path):
    full_audio = AudioSegment.from_file(audio_path)
    return len(full_audio)

def process_audio_segments(rttm_dict, audio_path, model, language, output_file="transcriptions.txt"):
    # Load entire audio file
    full_audio = AudioSegment.from_file(audio_path)
    
    with open(output_file, 'w', encoding="utf-8") as file:
        for line_num, segment in rttm_dict.items():
            # Convert seconds to milliseconds for pydub
            start_ms = int(segment['time_of_start'] * 1000)
            end_ms = int(segment['time_of_end'] * 1000)
            
            # Extract audio segment
            audio_segment = full_audio[start_ms:end_ms]
            
            # Save temporary audio segment
            temp_path = f"temp_{line_num}.wav"
            audio_segment.export(temp_path, format="wav")
            
            # Transcribe with Whisper
            transcription = model.get_text(temp_path, language, True)
            # Write to file
            print(temp_path)
            print(transcription)
            print(segment["time_of_start"])
            print(segment["time_of_end"])
            file.write(f"({segment['speaker_id']} from {segment['time_of_start']} to {segment['time_of_end']}): {transcription['text']}\n")

           
            os.remove(temp_path)
    return output_file

def adjust_audio(audio_path, destination_file):
    
    # Resample to 16kHz if necessary and Downmix to mono if necessary
    audio:AudioSegment = AudioSegment.from_file(audio_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    
    # Save the converted audio
    audio.export(destination_file, format="wav")
    
def rttm_join_speakers (file_path):
    rttm_file = file_path
    df = pd.read_csv(rttm_file, sep=" ", header=None, names=[
        "type", "file_id", "channel", "start_time", "duration", 
        "orthography", "speaker_type", "speaker_id", "extra1", "extra2"
    ])

    # Group consecutive segments by speaker ID
    merged_segments = []
    current_speaker = None
    current_start = None
    current_duration = 0

    for _, row in df.iterrows():
        if row["speaker_id"] == current_speaker:
            # If same speaker, add duration
            current_duration += row["duration"]
        else:
            # If new speaker, save previous segment
            if current_speaker is not None:
                current_duration = "{:.3f}".format(current_duration)
                merged_segments.append({
                    "type": "SPEAKER",
                    "file_id": row["file_id"],
                    "channel": row["channel"],
                    "start_time": current_start,
                    "duration": current_duration,
                    "orthography": "<NA>",
                    "speaker_type": "<NA>",
                    "speaker_id": current_speaker
                })
            
            # Start new segment
            current_speaker = row["speaker_id"]
            current_start = row["start_time"]
            current_duration = row["duration"]

    # Add the last segment
    merged_segments.append({
        "type": "SPEAKER",
        "file_id": df.iloc[-1]["file_id"],
        "channel": df.iloc[-1]["channel"],
        "start_time": current_start,
        "duration": current_duration,
        "orthography": "<NA>",
        "speaker_type": "<NA>",
        "speaker_id": current_speaker
    })

    # Create new DataFrame
    merged_df = pd.DataFrame(merged_segments)

    # Save back to RTTM format
    path = os.path.join(IN_PROCESS_DIR,f"merged_{os.path.splitext(os.path.basename(file_path))[0]}.rttm")

    merged_df.to_csv(path, sep=" ", header=False, index=False, 
                    columns=["type", "file_id", "channel", "start_time", "duration", 
                            "orthography", "speaker_type", "speaker_id"])

    print("Merged RTTM file saved as merged_output.rttm")
    
    
def parse_rttm(file_path):
    """
    Parses an RTTM file and stores each line's relevant info in a dictionary.

    Args:
        file_path (str): Path to the RTTM file.

    Returns:
        dict: A dictionary where keys are line numbers (starting from 1),
              and values are dictionaries with keys:
              'time_of_start', 'time_of_end', 'duration', 'speaker_id'.
    """
    data = {}

    with open(file_path, 'r') as f:
        for idx, line in enumerate(f, start=1):
            # Strip and split line by whitespace
            parts = line.strip().split()

            # Expected format:
            # Type file_name channel time_of_start duration <NA> <NA> speaker_id <NA> <NA>
            # So parts[3] = time_of_start, parts[4] = duration, parts[7] = speaker_id
            time_of_start = float(parts[3])
            duration = float(parts[4])
            time_of_end = time_of_start + duration
            speaker_id = parts[7]

            data[idx] = {
                'time_of_start': time_of_start,
                'time_of_end': time_of_end,
                'duration': duration,
                'speaker_id': speaker_id
            }

    return data


