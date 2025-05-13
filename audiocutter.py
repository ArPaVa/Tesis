from pydub import AudioSegment

def cut_audio(input_file, output_file, start_time, end_time):
    """
    Cuts a segment from an audio file and saves it as a new file.

    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the output audio file.
        start_time (float): Start time in seconds.
        end_time (float): End time in seconds.
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Convert start and end times to milliseconds
    start_ms = start_time * 1000
    end_ms = end_time * 1000

    # Slice the audio
    cut_segment = audio[start_ms:end_ms]

    # Export the sliced segment to a new file
    cut_segment.export(output_file, format="wav")
    print(f"Audio successfully saved to {output_file}")

# Example usage
input_audio = "longtesttocut.mp3"  # Replace with your input file path
output_audio = "mtest.wav"  # Replace with your desired output file path

# Cut the first 5 minutes (0 seconds to 300 seconds)
cut_audio(input_audio, output_audio, start_time=0, end_time=300)