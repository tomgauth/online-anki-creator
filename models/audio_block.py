from gtts import gTTS
from gtts import gTTS
import time
from moviepy.editor import concatenate_audioclips, AudioFileClip
import random
import os
import subprocess
import string
from models.block import Block


class AudioBlock:
    # takes a Block object and parameters and generates an audio block
    # the params required the following parameters: 
    # silence_between_repeat = int
    # silence_between_blocks_duration = int
    # repeat_1 = int
    # repeat_2 = int
    # block_type = str (recall, repeat, recognize)

    def __init__(self, block, **params: dict):
        self.block = block
        self.params = params
        self.validate_params()

    # a method that validates the parameters
    def validate_params(self):
        if not isinstance(self.params["silence_between_repeat"], int):
            return "Error: silence_between_repeat must be an integer"
        if not isinstance(self.params["silence_between_blocks_duration"], int):
            return "Error: silence_between_blocks_duration must be an integer"
        if not isinstance(self.params["repeat_1"], int):
            return "Error: repeat_1 must be an integer"
        if not isinstance(self.params["repeat_2"], int):
            return "Error: repeat_2 must be an integer"
        # block_type = str (recall, repeat, recognize)
        if self.params["block_type"] not in ["recall", "repeat", "recognize"]:
            return "Error: block_type must be one of the following: recall, repeat, recognize"


    @staticmethod
    def concatenate_silences(duration):
        # if the duration is not an integer or is zero, return an error
        silences_to_concat = []
        if not isinstance(duration, int) or duration == 0:
            return "Error: duration must be an integer greater than 0"
        for n in range(duration):
            silences_to_concat.append(AudioFileClip(f"staticfiles/silence_1s.mp3"))
        return concatenate_audioclips(silences_to_concat)
        
    def generate_explation(self, folder='staticfiles'):
        # generates an audio file with the explanation in the explanation language
        TTS_explanation = gTTS(text=self.block.explanation, lang=self.block.explanation_language)
        if self.block.explanation != "":
            TTS_explanation.save(f"{folder}/{self.block.explanation}_{self.block.explanation_language}.mp3")
            return AudioFileClip(f"{folder}/{self.block.explanation}_{self.block.explanation_language}.mp3")
     

    def generate_repeat_block(self):
        files_to_concat = []
        # generate an audio file with the phrase in language 1
        TTS_2 = gTTS(text=self.block.phrase_2, lang=self.block.language_2)
        TTS_2.save(f"staticfiles/{self.block.phrase_2}_{self.block.language_2}.mp3")
        # generate the silence files
        silence_between_repeat = self.concatenate_silences(self.params["silence_between_repeat"])
        silence_betwwen_blocks = self.concatenate_silences(self.params["silence_between_blocks_duration"])

        if self.params["repeat_1"] > 0:
            for n in range(self.params["repeat_1"]):
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_2}_{self.block.language_2}.mp3"))
                files_to_concat.append(silence_between_repeat)
        
        files_to_concat.append(silence_betwwen_blocks)

        final_clip = concatenate_audioclips(files_to_concat)

        return final_clip

    def generate_recognize_block(self):
        files_to_concat = []      
        # generate an audio file with the phrase in language 1           
        TTS_1 = gTTS(text=self.block.phrase_1, lang=self.block.origin_language)
        TTS_1.save(f"staticfiles/{self.block.phrase_1}_{self.block.origin_language}.mp3")
        # generate an audio file with the phrase in language 2
        TTS_2 = gTTS(text=self.block.phrase_2, lang=self.block.target_language)
        TTS_2.save(f"staticfiles/{self.block.phrase_2}_{self.block.target_language}.mp3")

        # generate the silence files
        silence_between_repeat = self.concatenate_silences(self.params["silence_between_repeat"])
        silence_between_phrases = self.concatenate_silences(self.params["silence_between_phrases_duration"])
        silence_between_blocks = self.concatenate_silences(self.params["silence_between_blocks_duration"])
        
        # if explanation, add the explation to the list of files to concatenate
        
        # add the first phrase to the list of files to concatenate number of times specified by repeat_1 adding a silence with the duration specified by silence_between_repeat        
        if self.params["repeat_2"] == 1:
            files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_2}_{self.block.target_language}.mp3"))
        else:
            for n in range(self.params["repeat_2"]):
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_2}_{self.block.target_language}.mp3"))
                files_to_concat.append(silence_between_repeat) 

        files_to_concat.append(silence_between_phrases)

        if self.params["repeat_1"] == 1:
            files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_1}_{self.block.origin_language}.mp3"))
        else:
            for n in range(self.params["repeat_1"]):            
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_1}_{self.block.origin_language}.mp3"))
                files_to_concat.append(silence_between_repeat)
        
        # add a silence with the duration specified by silence_between_phrases
        
        # add a silence with the duration specified by silence_between_blocks
        files_to_concat.append(silence_between_blocks)

        # concatenate all the files in the list
        final_clip = concatenate_audioclips(files_to_concat)
        # save the final clip
        # generate file name
        # file_name is a strng with the type of block name and 8 random characters
        return final_clip
        


    def generate_recall_block(self):
        files_to_concat = []      
        # generate an audio file with the phrase in language 1           
        TTS_1 = gTTS(text=self.block.phrase_1, lang=self.block.origin_language)
        TTS_1.save(f"staticfiles/{self.block.phrase_1}_{self.block.origin_language}.mp3")
        # generate an audio file with the phrase in language 2
        TTS_2 = gTTS(text=self.block.phrase_2, lang=self.block.target_language)
        TTS_2.save(f"staticfiles/{self.block.phrase_2}_{self.block.target_language}.mp3")

        # generate the silence files
        silence_between_repeat = self.concatenate_silences(self.params["silence_between_repeat"])
        silence_between_phrases = self.concatenate_silences(self.params["silence_between_phrases_duration"])
        silence_between_blocks = self.concatenate_silences(self.params["silence_between_blocks_duration"])
        
        # if explanation, add the explation to the list of files to concatenate
        
        # add the first phrase to the list of files to concatenate number of times specified by repeat_1 adding a silence with the duration specified by silence_between_repeat        
        if self.params["repeat_1"] == 1:
            files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_1}_{self.block.origin_language}.mp3"))
        else:
            for n in range(self.params["repeat_1"]):            
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_1}_{self.block.origin_language}.mp3"))
                files_to_concat.append(silence_between_repeat)
        
        # add a silence with the duration specified by silence_between_phrases
        files_to_concat.append(silence_between_phrases)

        # add the second phrase to the list of files to concatenate number of times specified by repeat_2 adding a silence with the duration specified by silence_between_repeat
        if self.params["repeat_2"] == 1:
            files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_2}_{self.block.target_language}.mp3"))
        else:
            for n in range(self.params["repeat_2"]):
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_2}_{self.block.target_language}.mp3"))
                files_to_concat.append(silence_between_repeat)
        
        # add a silence with the duration specified by silence_between_blocks
        files_to_concat.append(silence_between_blocks)

        # concatenate all the files in the list
        final_clip = concatenate_audioclips(files_to_concat)
        # save the final clip
        # generate file name
        # file_name is a strng with the type of block name and 8 random characters
        return final_clip
        # self.file_name = f"{self.params["block_type"]}_{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
        # final_clip.write_audiofile(f"staticfiles/{self.file_name}.mp3")
        # return f"staticfiles/{self.file_name}.mp3"

    def generate_audio_block(self):
        # generates an audio block from the details of the block
        if self.params["block_type"] == "repeat":
            return self.generate_repeat_block()
        elif self.params["block_type"] == "recognize":
            return self.generate_recognize_block()
        elif self.params["block_type"] == "recall":
            return self.generate_recall_block()
        else:
            return None



def test_block():
    # create a block using the block model from models.block
    block = Block(
        block_type="repeat",
        origin_language="EN-US",
        target_language="FR",
        phrase_1="Hello",
        phrase_2="Bonjour",
        explanation="",
        params = {
            "repeat_1": 1,
            "repeat_2": 2,
            "silence_between_repeat": 1,
            "silence_between_phrases_duration": 2,
            "silence_between_blocks_duration": 3            
        }      
    )
    # create an audio block using the block
    audio_block = AudioBlock(block)
    # generate the audio block
    audio_block.generate_audio_block()
    # save the audio block
    audio_block.save_audio_block()
    # return the file name
    return audio_block.file_name
