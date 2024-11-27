import os
import re
from pydub import AudioSegment
from tqdm import tqdm  # Import tqdm for the progress bar

def extract_audio(input_mkv, output_mp3):
    try:
        # Extract audio from MKV and convert to WAV using ffmpeg
        temp_wav = input_mkv.replace(".mkv", ".wav")
        command = f"ffmpeg -i \"{input_mkv}\" -vn -acodec pcm_s16le \"{temp_wav}\""
        os.system(command)

        # Convert the WAV to MP3 using pydub
        audio = AudioSegment.from_wav(temp_wav)
        audio.export(output_mp3, format="mp3")

        # Remove temporary WAV file
        os.remove(temp_wav)
        print(f"Audio successfully extracted and saved as {output_mp3}")
    except Exception as e:
        print(f"An error occurred with {input_mkv}: {e}")

def process_directory(video_folder, audio_folder):
    # Check if the audio folder exists, if not, create it
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)
    
    # Get all MKV files in the video folder
    video_files = [f for f in os.listdir(video_folder) if f.endswith(".mkv")]

    # Initialize the progress bar with the total number of files
    for filename in tqdm(video_files, desc="Processing files", unit="file"):
        # Extract the "S[number]E[number]" part of the filename using regex
        match = re.search(r'S\d+E\d+', filename)
        if match:
            episode_code = match.group(0)  # Extract the pattern like "S2E01"
        else:
            episode_code = "Unknown"  # Default if pattern isn't found

        # Define full file paths
        input_file = os.path.join(video_folder, filename)
        output_file = os.path.join(audio_folder, f"{episode_code}.mp3")

        # Call the extract_audio function for each file
        extract_audio(input_file, output_file)

# Example usage
video_folder = "Videos"  # Folder where MKV videos are stored
audio_folder = "Extrated_Audios"  # Folder where MP3 files will be saved
process_directory(video_folder, audio_folder)
