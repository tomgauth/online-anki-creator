from typing import List
from models.lesson import Lesson
from models.anki_model import anki_template
import genanki
import random
import os
from gtts import gTTS
from services.language_code_handler import CodeValidator


# Takes a Lesson and generates an Anki deck




class AnkiDeckGenerator():
    """a class that generates an Anki deck from a lesson
    takes a Lesson object, a anki model and a dictionary of parameters    
    """
    def __init__(self, lesson: Lesson, anki_template, params: dict):
        self.lesson = lesson
        self.anki_template = anki_template
        self.params = params
    
    def text_to_audio(self, text, language):
        # create a string that will be used to create the audio file name
        audio_file_name = text.replace(" ", "_") + ".mp3"
        # create a string that will be used to create the audio file path
        audio_file_path = f"staticfiles/{audio_file_name}"
        # if the audio file does not exist then create it
        if not os.path.exists(audio_file_path):
            # create an audio file using the google text to speech API            
            tts = gTTS(text, lang=language)
            tts.save(audio_file_path)
        return audio_file_name
    
    def generate_deck(self):
        # similar to the function above but with audio
        # for each row in the table, create an audio file for each language using the text_to_audio function
        # then add the audio file to the note
        origin_language = CodeValidator(self.lesson.origin_language).deepl_to_google()
        target_language = CodeValidator(self.lesson.target_language).deepl_to_google()
        deck_title = self.lesson.lesson_name
        anki_id = random.randrange(1 << 30, 1 << 31)
        my_deck = genanki.Deck(anki_id, deck_title)
        package = genanki.Package(my_deck)
        for row in self.lesson.content.split("\n"):
            row = row.split(";")
            print(row)
            if self.params["audio"]:
                # create the audio file for language one
                audio_file_one = self.text_to_audio(row[0], origin_language)
                audio_one = '[sound:{}]'.format(audio_file_one)
                print(audio_file_one)
                # create the audio file for language two
                audio_file_two = self.text_to_audio(row[1], target_language)
                audio_two = '[sound:{}]'.format(audio_file_two)
                # add the audio files to the note
                package.media_files.append(f'staticfiles/{audio_file_one}')
                package.media_files.append(f'staticfiles/{audio_file_two}')
            else:
                audio_one = ""
                audio_two = ""
            # if there is a 3rd column in the row then add it to the note
            comment = row[2] if len(row) == 3 else ""            
            try:
                note = genanki.Note(
                        model = self.anki_template,
                        fields = [row[0], row[1], comment, audio_one, audio_two]
                    )
            except IndexError:
                pass
            my_deck.add_note(note)
        package.write_to_file(f"{deck_title}.apkg")
        return f"{deck_title}.apkg"
    


def test_anki_deck_generator():
    # test the AnkiDeckGenerator class
    lesson = Lesson(
            lesson_name="test one",
            origin_language="EN-GB",
            target_language="FR",
            content="Greetings;Salutations\nHow are you?;Comment allez-vous?\nGoodbye;Au revoir\nsalut;hello; this is also a way to say goodbye""",
            intro="Intro to lesson one",
            outro="Outro to lesson one",
        )
    lesson.generate_blocks()
    deck_generator = AnkiDeckGenerator(lesson, anki_template, params={"audio": True})
    return deck_generator.generate_deck()
    