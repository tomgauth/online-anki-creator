import openai
import os
from controllers.translation_controller import TranslationController
import streamlit as st


if "open_ai_api_key.txt" in os.listdir():
    with open("open_ai_api_key.txt", "r") as f:
        api_key = f.read()
else:
    api_key = st.text_input("OpenAI API key", type="password", key="open_ai_api_key")

openai.api_key = api_key

class AiTrancriber():

    def __init__(self, audio_file_name, target_language, prompt_text=f"""
        Break down the following transcript into short phrases and sentences. Each phrase should be on a new line.      
        transcript:        
        """):
        self.audio_file_name = audio_file_name
        self.target_language = target_language
        self.prompt_text = prompt_text
        self.transcription_model = "whisper-1"
        self.audio_file = None        
    
    def open_audio_file(self):
        # if the format of audio_file_name is a string, open the file
        if isinstance(self.audio_file_name, str):
            self.audio_file = open(self.audio_file_name, "rb")
        else:
            self.audio_file = self.audio_file_name

    def transcribe(self):
        self.open_audio_file()
        print("transcribing audio file")
        transcript = openai.Audio.transcribe(self.transcription_model, self.audio_file)
        print("transcript: ", transcript)
        return transcript
    