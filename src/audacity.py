from settings import *
import os
import time
import pyaudacity as pa

# https://github.com/asweigart/pyaudacity
# https://manual.audacityteam.org/man/scripting_reference.html

def create_audacity_project_edited(audio_file_path, segments, output_project_path):

    gap = 3.0  # seconds of silence between clips
    offset = 0.0
    prev_lengths = []
    pa.do(f'Import2: Filename="{audio_file_path}"')

    for i, (start, end) in enumerate(segments):
        pa.select_time(start, end)
        pa.do('Duplicate')

        if i == 0:

            elapsed = end - start
        else:

            offset = sum(prev_lengths) + gap * i
            elapsed = end - start
        prev_lengths.append(elapsed)

        pa.do(f'Select: Start={offset} End={offset} RelativeTo="ProjectStart" Track={i+1} TrackCount=1')
        pa.do('Align_StartToSelStart')

        pa.do('SelectTracks: Track=0 TrackCount=1')

    pa.do(f'SaveProject2: Filename={output_project_path}')
    
    print(f"Audacity project saved to {output_project_path}")

def create_audacity_project_label_approach(audio_file_path, segments, output_project_path):
    """
    Creates an Audacity project with predefined segments selected.
    
    Args:
        audio_file_path (str): Path to the audio file.
        segments (list of tuples): List of (start_time, end_time) segments in seconds.
        output_project_path (str): Path to save the Audacity project (.aup3 file).
    """
    # Open Audacity and import the audio file
    pa.do(f'Import2: Filename={audio_file_path}')
    print("File imported")
    # Wait for the file to load (adjust delay if needed)
    pa.do('Select: Start=0 End=0')  # Small operation to ensure sync
    print("Small operation to ensure sync")
    
    # For each segment, select the region
    for i, (start, end) in enumerate(segments):
        # Select the segment
        pa.do(f'Select: Start={start} End={end}')
        print(f"Select: Start={start} End={end}")
        
        # Optional: Add a label for the segment (requires Audacity's Label Track)
        pa.do(f'AddLabel: Label={i+1}: {start}-{end}')
        print(f"AddLabel: Label={i+1}: {start}-{end}")
    
    # Save the Audacity project
    pa.do(f'SaveProject2: Filename={output_project_path}')
    
    print(f"Audacity project saved to {output_project_path}")
