from gtts import gTTS
# import google.cloud.texttospeech as tts
import random
import os



# if "google_tts_api_key.txt" in os.listdir():
#     with open("google_tts_api_key.txt", "r") as f:
#         google_tts_api_key = f.read()


class TextToSpeech:
    def __init__(self):
        pass

    @staticmethod
    def generate_silence(duration):
        duration = round(duration, 2)
        if not os.path.isfile("staticfiles/silence_{}.mp3".format(duration)):
            os.system("ffmpeg -f lavfi -i anullsrc -n -ab 128k -ar 44100 -ac 2 -t {} silence_{}.mp3".format(duration,duration))
        return "silence_{}.mp3".format(duration)
            

    @staticmethod        
    def text_to_audio(text, language):
        # create a string that will be used to create the audio file name
        audio_file_name = text.replace(" ", "_") + ".mp3"
        # create a string that will be used to create the audio file path
        audio_file_path = f"staticfiles/{audio_file_name}"
        # if the audio file does not exist then create it
        if not os.path.exists(audio_file_path):
            # create an audio file using the google text to speech API
            tts = gTTS(text, lang=language)
            tts.save(audio_file_path)
        return audio_file_path
    