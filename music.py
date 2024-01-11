from pydub import AudioSegment
import os

# Directory containing the mixed audio files
mixed_audio_folder = "mixed"

# Get a list of all audio files in the directory
audio_files = [file for file in os.listdir(mixed_audio_folder) if file.endswith(".mp3")]

# Initialize an empty AudioSegment
combined_audio = AudioSegment.silent(duration=0)

# Loop through each audio file and concatenate them
for audio_file in audio_files:
    audio_path = os.path.join(mixed_audio_folder, audio_file)
    segment = AudioSegment.from_file(audio_path, format="mp3")
    combined_audio += segment

# Export the combined audio to a single file
combined_audio.export("combined_audio.mp3", format="mp3")

combined_audio = AudioSegment.from_file('combined_audio.mp3', format="mp3")

# Load the background music with lower volume
bg_music = AudioSegment.from_file('bg.mp3', format="mp3")
bg_music = bg_music - 20  # Decrease volume (adjust this value as needed)

# Overlay the background music on the combined audio
final_audio = combined_audio.overlay(bg_music)

# Export the final audio with background music
final_audio.export("final_audio.mp3", format="mp3")