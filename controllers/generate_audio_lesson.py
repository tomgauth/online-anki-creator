from gtts import gTTS
import time
from moviepy.editor import concatenate_audioclips, AudioFileClip
import random
import os
import subprocess
import string
from models.block import Block
from models.lesson import Lesson
from services.language_code_handler import CodeValidator


# a controller that takes a lesson and parameters and generates an audio file with the lesson
class AudioLessonGenerator():
    # takes a Lesson object and parameters and generates an audio file with the lesson
    def __init__(self, lesson: Lesson, params: dict):
        self.lesson = lesson
        self.params = params
        self.validate_params()
        self.audio_lesson = None
    

    # a method that validates the parameters
    def validate_params(self):
        if not isinstance(self.params["read_intro"], bool):
            return "Error: read_intro must be a boolean"
        # read_outro shoud be a boolean
        if not isinstance(self.params["read_outro"], bool):
            return "Error: read_outro must be a boolean"
        if not isinstance(self.params["silence_between_phrases_duration"], int):
            return "Error: silence_between_phrases_duration must be an integer"
        if not isinstance(self.params["silence_between_blocks_duration"], int):
            return "Error: silence_between_blocks_duration must be an integer"
        if not isinstance(self.params["repeat_1"], int):
            return "Error: repeat_1 must be an integer"
        if not isinstance(self.params["repeat_2"], int):
            return "Error: repeat_2 must be an integer"
        # block_type = str (recall, repeat, recognize)
        if self.params["block_type"] not in ["recall", "repeat", "recognize"]:
            return "Error: block_type must be one of the following: recall, repeat, recognize"
    
    def generate_intro_outro(self):
        intro = ""
        outro = ""

        # generate the intro and outro audio files
        lang = CodeValidator(self.lesson.origin_language).deepl_to_google()     
        intro_audio = gTTS(text=intro, lang=lang, slow=False)
        intro_audio.save("intro.mp3")
        outro_audio = gTTS(text=outro, lang=lang, slow=False)
        outro_audio.save("outro.mp3")
        return intro_audio, outro_audio

    # Creates blocks for the lesson
    # Converts the blocks into audio blocks using the AudioBlockGenerator class and the parameters
    # Concatenates the audio blocks into a single audio file
    def generate_audio_lesson(self):        
        self.lesson.generate_blocks()
        audio_blocks = []

        if self.params["read_intro"]:
            lang = CodeValidator(self.lesson.origin_language).deepl_to_google()   
            intro_audio = gTTS(text=self.lesson.intro, lang=lang, slow=False)
            intro_audio = gTTS(text=self.lesson.intro, lang=lang, slow=False)
            intro_audio.save("intro.mp3")
            audio_blocks.append(AudioFileClip("intro.mp3"))

        for block in self.lesson.blocks:
            audio_block_generator = AudioBlockGenerator(block, self.params)
            audio_blocks.append(audio_block_generator.generate_audio_block())

        if self.params["read_outro"]:
            lang = CodeValidator(self.lesson.origin_language).deepl_to_google()
            outro_audio = gTTS(text=self.lesson.outro, lang=lang, slow=False)
            outro_audio.save("outro.mp3")
            audio_blocks.append(AudioFileClip("outro.mp3"))
        
        # concatenate the audio blocks
        self.audio_lesson = concatenate_audioclips(audio_blocks)
        # converts the audio file to mp3
        self.audio_lesson.write_audiofile(f"{self.lesson.lesson_name}.mp3", codec="libmp3lame", bitrate="320k")
        return f"{self.lesson.lesson_name}.mp3"

        




class AudioBlockGenerator():
    # takes a Block object and parameters and generates an audio block
    # the params required the following parameters: 
    # silence_between_repeat = int
    # silence_between_blocks_duration = int
    # repeat_1 = int
    # repeat_2 = int
    # block_type = str (recall, repeat, recognize)

    def __init__(self, block, params: dict):
        self.block = block
        self.params = params
        self.audio_block = None
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
            silences_to_concat.append(AudioFileClip(f"staticfiles/silence_1.mp3"))
        return concatenate_audioclips(silences_to_concat)
        
    def generate_explation(self, folder='staticfiles'):
        # generates an audio file with the explanation in the explanation language
        explanation_language = CodeValidator(self.block.explanation_language).deepl_to_google()
        TTS_explanation = gTTS(text=self.block.explanation, lang=explanation_language)
        if self.block.explanation != "":
            TTS_explanation.save(f"{folder}/{self.block.explanation}_{explanation_language}.mp3")
            return AudioFileClip(f"{folder}/{self.block.explanation}_{explanation_language}.mp3")
     

    def generate_repeat_block(self):
        files_to_concat = []
        # generate an audio file with the phrase in language 1
        target_language = CodeValidator(self.block.target_language).deepl_to_google()
        TTS_2 = gTTS(text=self.block.phrase_2, lang=target_language)
        TTS_2.save(f"staticfiles/{self.block.phrase_2}_{target_language}.mp3")
        # generate the silence files
        silence_between_repeat = self.concatenate_silences(self.params["silence_between_repeat"])
        silence_betwwen_blocks = self.concatenate_silences(self.params["silence_between_blocks_duration"])

        if self.params["repeat_1"] > 0:
            for n in range(self.params["repeat_1"]):
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_2}_{target_language}.mp3"))
                files_to_concat.append(silence_between_repeat)
        
        files_to_concat.append(silence_betwwen_blocks)

        final_clip = concatenate_audioclips(files_to_concat)
        self.audio_block = final_clip
        return final_clip

    def generate_recognize_block(self):
        files_to_concat = []      
        # generate an audio file with the phrase in language 1     
        origin_language = CodeValidator(self.block.origin_language).deepl_to_google()
        target_language = CodeValidator(self.block.target_language).deepl_to_google()
        TTS_1 = gTTS(text=self.block.phrase_1, lang=origin_language)
        TTS_1.save(f"staticfiles/{self.block.phrase_1}_{origin_language}.mp3")
        # generate an audio file with the phrase in language 2
        TTS_2 = gTTS(text=self.block.phrase_2, lang=target_language)
        TTS_2.save(f"staticfiles/{self.block.phrase_2}_{target_language}.mp3")

        # generate the silence files
        silence_between_repeat = self.concatenate_silences(self.params["silence_between_repeat"])
        silence_between_phrases = self.concatenate_silences(self.params["silence_between_phrases_duration"])
        silence_between_blocks = self.concatenate_silences(self.params["silence_between_blocks_duration"])
        
        # if explanation, add the explation to the list of files to concatenate
        
        # add the first phrase to the list of files to concatenate number of times specified by repeat_1 adding a silence with the duration specified by silence_between_repeat        
        if self.params["repeat_2"] == 1:
            files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_2}_{target_language}.mp3"))
        else:
            for n in range(self.params["repeat_2"]):
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_2}_{target_language}.mp3"))
                files_to_concat.append(silence_between_repeat) 

        files_to_concat.append(silence_between_phrases)

        if self.params["repeat_1"] == 1:
            files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_1}_{origin_language}.mp3"))
        else:
            for n in range(self.params["repeat_1"]):            
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_1}_{origin_language}.mp3"))
                files_to_concat.append(silence_between_repeat)
        
        # add a silence with the duration specified by silence_between_phrases
        
        # add a silence with the duration specified by silence_between_blocks
        files_to_concat.append(silence_between_blocks)

        # concatenate all the files in the list
        final_clip = concatenate_audioclips(files_to_concat)
        self.audio_block = final_clip
        # save the final clip
        # generate file name
        # file_name is a strng with the type of block name and 8 random characters
        return final_clip
        


    def generate_recall_block(self):
        files_to_concat = []      
        # generate an audio file with the phrase in language 1
        origin_language = CodeValidator(self.block.origin_language).deepl_to_google()
        target_language = CodeValidator(self.block.target_language).deepl_to_google()
        TTS_1 = gTTS(text=self.block.phrase_1, lang=origin_language)
        TTS_1.save(f"staticfiles/{self.block.phrase_1}_{origin_language}.mp3")
        # generate an audio file with the phrase in language 2
        TTS_2 = gTTS(text=self.block.phrase_2, lang=target_language)
        TTS_2.save(f"staticfiles/{self.block.phrase_2}_{target_language}.mp3")

        # generate the silence files
        silence_between_repeat = self.concatenate_silences(self.params["silence_between_repeat"])
        silence_between_phrases = self.concatenate_silences(self.params["silence_between_phrases_duration"])
        silence_between_blocks = self.concatenate_silences(self.params["silence_between_blocks_duration"])
        
        # if explanation, add the explation to the list of files to concatenate
        
        # add the first phrase to the list of files to concatenate number of times specified by repeat_1 adding a silence with the duration specified by silence_between_repeat        
        if self.params["repeat_1"] == 1:
            files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_1}_{origin_language}.mp3"))
        else:
            for n in range(self.params["repeat_1"]):            
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_1}_{origin_language}.mp3"))
                files_to_concat.append(silence_between_repeat)
        
        # add a silence with the duration specified by silence_between_phrases
        files_to_concat.append(silence_between_phrases)

        # add the second phrase to the list of files to concatenate number of times specified by repeat_2 adding a silence with the duration specified by silence_between_repeat
        if self.params["repeat_2"] == 1:
            files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_2}_{target_language}.mp3"))
        else:
            for n in range(self.params["repeat_2"]):
                files_to_concat.append(AudioFileClip(f"staticfiles/{self.block.phrase_2}_{target_language}.mp3"))
                files_to_concat.append(silence_between_repeat)
        
        # add a silence with the duration specified by silence_between_blocks
        files_to_concat.append(silence_between_blocks)

        # concatenate all the files in the list
        final_clip = concatenate_audioclips(files_to_concat)
        self.audio_block = final_clip
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
        origin_language="EN-GB",
        target_language="FR",
        phrase_1="Hello",
        phrase_2="Bonjour",
        explanation=""   
    )
    params = {
        "block_type": "repeat",
        "repeat_1": 1,
        "repeat_2": 2,
        "silence_between_repeat": 1,
        "silence_between_phrases_duration": 2,
        "silence_between_blocks_duration": 3            
    }   
    # create an audio block using the block
    audio_block = AudioBlockGenerator(block, params)
    # generate the audio block
    audio_block.generate_audio_block()
    return audio_block


def test_audio_lesson():
    # create a Lesson object
    lesson = Lesson(
        lesson_name="test one",
        origin_language="EN-GB",
        target_language="FR",
        content="Hello;Bonjour\nHow are you?;Comment allez-vous?\nGoodbye;Au revoir\nsalut;hello; this is also a way to say goodbye""",
        intro="Intro to lesson one",
        outro="Outro to lesson one",
    )
    lesson_params = {
        "intro" : "intro to lesson one",
        "outro" : "outro to lesson one",
        "generate_explanation" : True,
        "read_intro" : True,
        "read_outro" : False,
        "silence_between_repeat" : 2,
        "silence_between_phrases_duration" : 1,
        "silence_between_blocks_duration" : 2,
        "repeat_1" : 2,
        "repeat_2" : 1,
        "block_type" : "recall"
        }
    # create an audio lesson using the lesson
    audio_lesson = AudioLessonGenerator(lesson, lesson_params)
    # generate the audio lesson
    audio_lesson.generate_audio_lesson()
    return audio_lesson