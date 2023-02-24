from gtts import gTTS
from gtts import gTTS
import time
from moviepy.editor import concatenate_audioclips, AudioFileClip
import ffmpeg
import random
import os
import subprocess

# generates an audio file from a text file using the gTTS library

# takes input from a streamlit text_input and returns it back to the user

# ttss = TextToSpeechService("hello ; bonjour", "en", "fr", "hello", ";", 2,1,True)

def generate_silence(duration, folder='staticfiles'):
    # Set the audio format, sample rate, and number of channels
    audio_format = 'mp3'
    sample_rate = 44100
    channels = 2
    
    # Set the output filename and path
    output_filename = f'{folder}/silence_{duration}s.mp3'
    
    # Set the duration of the silence in seconds
    duration = int(duration)
    
    # Generate the FFmpeg command
    command = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate={}'.format(sample_rate), '-t', str(duration), '-q:a', '9', '-ac', str(channels), '-ar', str(sample_rate), output_filename]
    
    # Execute the FFmpeg command
    subprocess.run(command)

class TextToSpeechService:
    # the constructor takes the form data as an argument and assigns it to the instance    
    def __init__(self, text, language_1, language_2, file_name, separator, silence_between_phrases_duration, silence_between_blocks_duration, shuffle_blocks):
        self.text = text
        self.language_1 = language_1
        self.language_2 = language_2
        self.file_name = file_name
        self.separator = separator
        self.silence_between_phrases_duration = silence_between_phrases_duration
        self.silence_between_blocks_duration = silence_between_blocks_duration
        self.shuffle_blocks = shuffle_blocks
        self.text = text
        self.lines = [line.split(separator) for line in self.text.splitlines()]
        self.blocks_to_concat = []        

    def generate_blocks(self):
        for line in self.lines:
            lines_to_concat = []
            # generate a text to speech file using the language 1 and save it to the static folder            
            TTS_1 = gTTS(text=line[0], lang=self.language_1)
            file_1_name = f"staticfiles/{line[0]}_{self.language_1}.mp3"
            TTS_1.save(file_1_name)
            lines_to_concat.append(AudioFileClip(file_1_name))
            for n in range(self.silence_between_phrases_duration):
                lines_to_concat.append(AudioFileClip(f"staticfiles/silence_1s.mp3"))
            # do the same for language 2
            TTS_2 = gTTS(text=line[1], lang=self.language_2)
            file_2_name = f"staticfiles/{line[1]}_{self.language_2}.mp3"
            TTS_2.save(f"staticfiles/{line[1]}_{self.language_2}.mp3")
            lines_to_concat.append(AudioFileClip(file_2_name))
            # concatenate the audio files using ffmpeg with the silence_between_phrases file            
            for n in range(self.silence_between_blocks_duration):
                lines_to_concat.append(AudioFileClip(f"staticfiles/silence_1s.mp3"))
            block = concatenate_audioclips(lines_to_concat)
            self.blocks_to_concat.append(block)
        
    def concatenate_blocks(self):
        if self.shuffle_blocks:
            self.perform_shuffle_blocks()
        self.create_audio_file()
        

    def perform_shuffle_blocks(self):
        random.shuffle(self.blocks_to_concat)

    def create_audio_file(self):
        final_audio = concatenate_audioclips(self.blocks_to_concat)
        final_audio.write_audiofile(f"{self.file_name}.mp3")
    
    def get_audio_file(self):
        return f"{self.file_name}.mp3"
    
    def delete_audio_files(self):
        # remove all the files in the staticfiles folder except the silence_1s.mp3 file
        for file in os.listdir("staticfiles"):
            if file != "silence_1s.mp3":
                os.remove(f"staticfiles/{file}")