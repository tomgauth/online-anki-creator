from gtts import gTTS
from gtts import gTTS
import time
from moviepy.editor import concatenate_audioclips, AudioFileClip
import random
import os
import subprocess
import string

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


class AudioBlock:
    # an AudioBlock takes the following elements:
    # - a phrase in language 1
    # - a phrase in language 2 or None
    # - a silence duration between the two phrases
    # - a silence duration at the end of the block
    # - an explanation of the block
    # - a language for the explanation of the block
    # - a type of block (Repeat, Recognize, Recall)
    def __init__(self, phrase_1, phrase_2, repeat_1, repeat_2, silence_between_repeat, language_1, language_2, silence_between_phrases_duration, silence_between_blocks_duration, explanation, explanation_language, block_type):
        self.phrase_1 = phrase_1
        self.phrase_2 = phrase_2
        self.repeat_1 = repeat_1
        self.repeat_2 = repeat_2
        self.silence_between_repeat = silence_between_repeat
        self.language_1 = language_1
        self.language_2 = language_2
        self.silence_between_phrases_duration = silence_between_phrases_duration
        self.silence_between_blocks_duration = silence_between_blocks_duration
        self.explanation = explanation
        self.explanation_language = explanation_language
        self.block_type = block_type

    def details(self):
        # returns a multiline string with all the details of the block
        print(f"""phrase 1: {self.phrase_1}
phrase 2: {self.phrase_2}
repeat 1: {self.repeat_1}
repeat 2: {self.repeat_2}
silence_between_repeat: {self.silence_between_repeat}
language 1: {self.language_1}
language 2: {self.language_2}
silence between phrases: {self.silence_between_phrases_duration}
silence between blocks: {self.silence_between_blocks_duration}
explanation: {self.explanation}
explanation language: {self.explanation_language}
block type: {self.block_type}""")

    def visualize(self):
        # returns a linear visualization of the block
        if self.block_type == "Repeat":
            return f"""{self.phrase_1} x {self.repeat_1} times - {self.silence_between_repeat} seconds silence - {self.phrase_2} x {self.repeat_2} times - {self.silence_between_phrases_duration} seconds silence - {self.silence_between_blocks_duration} seconds silence"""
        pass
        

    def concatenate_silences(self, duration):
        # if the duration is not an integer or is zero, return an error
        silences_to_concat = []
        if not isinstance(duration, int) or duration == 0:
            return "Error: duration must be an integer greater than 0"
        for n in range(duration):
            silences_to_concat.append(AudioFileClip(f"staticfiles/silence_1s.mp3"))
        return concatenate_audioclips(silences_to_concat)
        
    def generate_explation(self, folder='staticfiles'):
        # generates an audio file with the explanation in the explanation language
        TTS_explanation = gTTS(text=self.explanation, lang=self.explanation_language)
        if self.explanation != "":
            TTS_explanation.save(f"staticfiles/{self.explanation}_{self.explanation_language}.mp3")
            return AudioFileClip(f"staticfiles/{self.explanation}_{self.explanation_language}.mp3")
     

    def generate_repeat_block(self):
        files_to_concat = []
        # generate an audio file with the phrase in language 1
        TTS_2 = gTTS(text=self.phrase_2, lang=self.language_2)
        TTS_2.save(f"staticfiles/{self.phrase_2}_{self.language_2}.mp3")
        # generate the silence files
        silence_between_repeat = self.concatenate_silences(self.silence_between_repeat)
        silence_betwwen_blocks = self.concatenate_silences(self.silence_between_blocks_duration)

        if self.repeat_1 > 0:
            for n in range(self.repeat_1):
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.phrase_2}_{self.language_2}.mp3"))
                files_to_concat.append(silence_between_repeat)
        
        files_to_concat.append(silence_betwwen_blocks)

        final_clip = concatenate_audioclips(files_to_concat)

        return final_clip



    def generate_recall_block(self):
        files_to_concat = []      
        # generate an audio file with the phrase in language 1           
        TTS_1 = gTTS(text=self.phrase_1, lang=self.language_1)
        TTS_1.save(f"staticfiles/{self.phrase_1}_{self.language_1}.mp3")
        # generate an audio file with the phrase in language 2
        TTS_2 = gTTS(text=self.phrase_2, lang=self.language_2)
        TTS_2.save(f"staticfiles/{self.phrase_2}_{self.language_2}.mp3")

        # generate the silence files
        silence_between_repeat = self.concatenate_silences(self.silence_between_repeat)
        silence_between_phrases = self.concatenate_silences(self.silence_between_phrases_duration)
        silence_between_blocks = self.concatenate_silences(self.silence_between_blocks_duration)
        
        # if explanation, add the explation to the list of files to concatenate
        
        # add the first phrase to the list of files to concatenate number of times specified by repeat_1 adding a silence with the duration specified by silence_between_repeat        
        if self.repeat_1 == 1:
            files_to_concat.append(AudioFileClip(f"staticfiles/{self.phrase_1}_{self.language_1}.mp3"))
        else:
            for n in range(self.repeat_1):            
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.phrase_1}_{self.language_1}.mp3"))
                files_to_concat.append(silence_between_repeat)
        
        # add a silence with the duration specified by silence_between_phrases
        files_to_concat.append(silence_between_phrases)

        # add the second phrase to the list of files to concatenate number of times specified by repeat_2 adding a silence with the duration specified by silence_between_repeat
        if self.repeat_2 == 1:
            files_to_concat.append(AudioFileClip(f"staticfiles/{self.phrase_2}_{self.language_2}.mp3"))
        else:
            for n in range(self.repeat_2):
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.phrase_2}_{self.language_2}.mp3"))
                files_to_concat.append(silence_between_repeat)
        
        # add a silence with the duration specified by silence_between_blocks
        files_to_concat.append(silence_between_blocks)

        # concatenate all the files in the list
        final_clip = concatenate_audioclips(files_to_concat)
        # save the final clip
        # generate file name
        # file_name is a strng with the type of block name and 8 random characters
        return final_clip
        # self.file_name = f"{self.block_type}_{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
        # final_clip.write_audiofile(f"staticfiles/{self.file_name}.mp3")
        # return f"staticfiles/{self.file_name}.mp3"

    def generate_audio_block(self):
        # generates an audio block from the details of the block
        if self.block_type == "repeat":
            return self.generate_repeat_block()
        elif self.block_type == "recognize":
            return self.generate_recognize_block()
        elif self.block_type == "recall":
            return self.generate_recall_block()
        else:
            return None
        

class TextToSpeechService:
    # the constructor takes the form data as an argument and assigns it to the instance    
    def __init__(self, text, language_1, language_2, file_name, separator, silence_between_phrases_duration, silence_between_blocks_duration, shuffle_blocks, block_type):
        self.text = text
        self.language_1 = language_1
        self.language_2 = language_2
        self.file_name = file_name
        self.separator = separator
        self.silence_between_phrases_duration = silence_between_phrases_duration
        self.silence_between_blocks_duration = silence_between_blocks_duration
        self.shuffle_blocks = shuffle_blocks
        self.block_type = block_type
        self.lines = [line.split(separator) for line in self.text.splitlines()]
        self.blocks_to_concat = []        

    def generate_blocks(self):
        for line in self.lines:
            block = AudioBlock( phrase_1 = line[0],
                phrase_2 = line[1],
                repeat_1 = 1,
                repeat_2 = 2,
                silence_between_repeat = 2,
                language_1 = self.language_1,
                language_2 = self.language_2,
                silence_between_phrases_duration = self.silence_between_phrases_duration,
                silence_between_blocks_duration = self.silence_between_blocks_duration,
                explanation = None,
                explanation_language = None,
                block_type = self.block_type
            )
            audio_block = block.generate_audio_block()                                                                                                                         
                               
            self.blocks_to_concat.append(audio_block)
        

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



def test_audio_block():
    # test the AudioBlock class
    # create an instance of the AudioBlock class
    block = AudioBlock(
        phrase_1="I understand", 
        phrase_2="Je comprends", 
        repeat_1=1, 
        repeat_2=2, 
        silence_between_repeat=1, 
        language_1="en", 
        language_2="fr", 
        silence_between_phrases_duration=3, 
        silence_between_blocks_duration=1, 
        explanation="The verb is understanding", 
        explanation_language="en", 
        block_type="recall")
    # generate the audio block
    block.generate_audio_block()
    # return the file name
    return block.file_name

def test_text_to_speech_service():
    # test the TextToSpeechService class
    # create an instance of the TextToSpeechService class
    text = "I understand ; Je comprends\nI don't understand ; Je ne comprends pas \nI don't know ; Je ne sais pas"
    service = TextToSpeechService(text, "en", "fr", "test", ";", 3, 1, True, "recall")
    # generate the blocks
    service.generate_blocks()
    # concatenate the blocks
    service.concatenate_blocks()
    # return the file name
    return service.get_audio_file()
