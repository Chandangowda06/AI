import shutil
from model import predict
from text_extraction import read_pdf
import pandas as pd
from gtts import gTTS
from pydub import AudioSegment
import os
from random import randint

def generate_audio(text, index):
    tts = gTTS(text=text, lang='en', slow=False)
    audio_path = f"audio/{index}.mp3"
    tts.save(audio_path)
    return audio_path

def mix_audio(tts_audio_path, emotion_audio_folder):
    # Load TTS audio
    tts_audio = AudioSegment.from_file(tts_audio_path, format="mp3")

    # Select a random emotion-specific music file if available
    emotion_audio_files = [f for f in os.listdir(emotion_audio_folder) if f.endswith(".mp3")]

    if emotion_audio_files:
        selected_emotion_audio = emotion_audio_files[randint(0, len(emotion_audio_files) - 1)]
        
        # Load the selected emotion-specific music
        emotion_audio = AudioSegment.from_file(os.path.join(emotion_audio_folder, selected_emotion_audio), format="mp3")
        emotion_audio = emotion_audio - 30
        # Mix TTS audio with emotion-specific music
        print("Mixing")
        mixed_audio = tts_audio.overlay(emotion_audio)
        return mixed_audio

    return tts_audio 

# Read PDF and predict emotions
sentences = read_pdf('PDF/l.pdf')
print(sentences)
emotions = predict(sentences)
df = pd.DataFrame({
    'sentences': sentences,
    'emotions': emotions
})

os.makedirs('audio')# Generate and save TTS audio for each sentence
os.makedirs('mixed')# Generate and save TTS audio for each sentence
for index, row in df.iterrows():
    sentence = row['sentences']
    emotion = row['emotions']
    print(sentence, emotion, sep='\n')
    tts_audio_path = generate_audio(sentence, index)
    print(tts_audio_path)
    # Mix TTS audio with corresponding emotion-specific music
    emotion_music_folder = os.path.join('music', emotion)
    print(emotion_music_folder)
    mixed_audio = mix_audio(tts_audio_path, emotion_music_folder)

    # Save the mixed audio for each emotion
    mixed_audio_path = os.path.join('mixed', f'{index}_mixed.mp3')
    mixed_audio.export(mixed_audio_path, format="mp3")

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

# Load the background music with lower volume
bg_music_folder = [file for file in os.listdir('bg') if file.endswith(".mp3")]
selected_bg_music = bg_music_folder[randint(0, len(bg_music_folder) - 1)]
bg_music = AudioSegment.from_file(os.path.join('bg', selected_bg_music), format="mp3")
bg_music = bg_music - 20  # Decrease volume (adjust this value as needed)

# Loop background music to match the duration of the combined audio
while len(bg_music) < len(combined_audio):
    bg_music += bg_music

# Trim background music to match the duration of the combined audio
bg_music = bg_music[:len(combined_audio)]

# Overlay the background music on the combined audio
final_audio = combined_audio.overlay(bg_music)

# Export the final audio with background music
final_audio.export("final_audio.mp3", format="mp3")

shutil.rmtree('mixed')
shutil.rmtree('audio')
print("done")