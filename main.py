import streamlit as st
import genanki
import random
from os.path import exists
import time
from gtts import gTTS
import os
from gen_audio import TextToSpeechService
from gen_pdf import PDFGenerator

SEPARATOR = ";"

# create a list of languages that can be used with the google text to speech API
language_list = ['af', 'sq', 'ar', 'hy', 'bn', 'ca', 'zh', 'zh-cn', 'zh-tw', 'zh-yue', 'hr', 'cs', 'da', 'nl', 'en', 'en-au', 'en-uk', 'en-us', 'eo', 'fi', 'fr', 'de', 'el', 'hi', 'hu', 'is', 'id', 'it', 'ja', 'ko', 'la', 'lv', 'mk', 'no', 'pl', 'pt', 'pt-br', 'ro', 'ru', 'sr', 'sk', 'es', 'es-es', 'es-us', 'sw', 'sv', 'ta', 'th', 'tr', 'vi', 'cy']


def gen_anki_id():
    return random.randrange(1 << 30, 1 << 31)



my_model = genanki.Model(
  gen_anki_id(),
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'Audio_one'},
    {'name': 'Audio_two'}
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}} </br> {{Audio_one}}',
      'afmt': '''{{FrontSide}}
      <hr id=answer>
        {{Audio_two}}
        <div style="font-family: Futura; font-size: 20px;">{{Answer}}</div>        
        <div style= "color:#00afe4; font-family: Futura; font-size: 10px;">©Online Anki Generator</div>''',
    },
  ])


# Create a function that will take some input from streamlit (st.text_input) and return it back to the user (st.write)



def txt_to_list_of_lists(text_input):
    table = [line.split(SEPARATOR) for line in text_input.split("\n")]
    # remove any empty lines
    table = [line for line in table if line != ['']]
    return table


def exists(file_name):
    try:
        with open(file_name):
            return True
    except IOError:
        return False


# create a function that takes a string and a language value and returns an audio file using the google text to speech API
def text_to_audio(text, language):
    # create a string that will be used to create the audio file name
    audio_file_name = text.replace(" ", "_") + ".mp3"
    # create a string that will be used to create the audio file path
    audio_file_path = f"{audio_file_name}"
    # if the audio file does not exist then create it
    if not exists(audio_file_path):
        # create an audio file using the google text to speech API
        tts = gTTS(text, lang=language)
        tts.save(audio_file_path)
    return audio_file_path




def to_anki_deck_no_audio(table, language_one, language_two, deck_title):
    my_deck = genanki.Deck(gen_anki_id(), deck_title)
    package = genanki.Package(my_deck) 
    i = 0
    my_bar = st.progress(i)
    for row in table:
        my_bar.progress(i/len(table))
        try:
            note = genanki.Note(
                    model = my_model,
                    fields = [row[0], row[1]],                    
                )
        except IndexError:
            pass
        my_deck.add_note(note)
    package.write_to_file(f"{deck_title}.apkg")
    return f"{deck_title}.apkg"


def to_anki_deck_with_audio(table, language_one, language_two, deck_title):
    # similar to the function above but with audio
    # for each row in the table, create an audio file for each language using the text_to_audio function
    # then add the audio file to the note
    my_deck = genanki.Deck(gen_anki_id(), deck_title)
    package = genanki.Package(my_deck)
    i = 0
    my_bar = st.progress(i)
    for row in table:
        # create the audio file for language one
        audio_file_one = text_to_audio(row[0], language_one)
        audio_one = '[sound:{}]'.format(audio_file_one)
        print(audio_file_one)
        # create the audio file for language two
        audio_file_two = text_to_audio(row[1], language_two)
        audio_two = '[sound:{}]'.format(audio_file_two)
        # add the audio files to the note
        my_bar.progress(i/len(table))
        try:
            note = genanki.Note(
                    model = my_model,
                    fields = [row[0], row[1], audio_one, audio_two]
                )
        except IndexError:
            pass
        package.media_files.append(audio_file_one)
        package.media_files.append(audio_file_two)
        my_deck.add_note(note)
    package.write_to_file(f"{deck_title}.apkg")
    return f"{deck_title}.apkg"

def cleanup():
    # delete all the audio files
    print("removing audio files and apkg files")
    for file in os.listdir():
        if file.endswith(".mp3"):
            os.remove(file)
        elif file.endswith(".apkg"):
            os.remove(file)
            

def main():    
    anki_deck = None
    audio_lesson = None
    pdf_lesson = None
    with st.form("input phrases"):
        st.title("Create your Anki Deck below!")
        # create 2 input fields called language one and language two for inputing the language as a string (5 characters max)
        # use a selector to select the language instead of a text input
        language_one = st.selectbox("Language One", language_list, index=14)        
        language_two = st.selectbox("Language Two", language_list, index=20)
        # create a toggle button to select if you want to use audio or not
        use_audio = st.checkbox("Use Audio")
        st.text("This is a simple text input, use ; to separate the fields")
        # create a text area for inputing the phrases with default text """bonjour ; hello
        # merci ; thank you"""
        content = st.text_area(label= "input your vocabulary" ,placeholder="""hello ; bonjour
thank you ; merci""", height=200)
        table = txt_to_list_of_lists(content)
        deck_title = title = st.text_input("Deck Title")
        submit_anki = st.form_submit_button("Generate Anki Deck")
        silence_between_blocks_duration = st.number_input("Silence between blocks duration", min_value=0, max_value=10, value=1)
        silence_between_phrases_duration = st.number_input("Silence between phrases duration", min_value=0, max_value=10, value=2)
        submit_audio = st.form_submit_button("Generate Audio")
        submit_pdf = st.form_submit_button("Generate PDF")
        # st.write(table)
        if submit_anki:
            if use_audio:
                anki_deck = to_anki_deck_with_audio(table, language_one, language_two, deck_title)
            else:
                anki_deck = to_anki_deck_no_audio(table, language_one, language_one, deck_title)   
        if submit_audio:
            ttss = TextToSpeechService(
                text=content,
                language_1=language_one,
                language_2=language_two,
                file_name=deck_title,
                separator=";",
                silence_between_blocks_duration=silence_between_blocks_duration,
                silence_between_phrases_duration=silence_between_phrases_duration,
                shuffle_blocks=True
                )
            ttss.generate_blocks()
            ttss.concatenate_blocks()
            ttss.create_audio_file()
            audio_lesson = ttss.get_audio_file()
        if submit_pdf:
            pdf_lesson = PDFGenerator(
                text=content,
                language_1=language_one,
                language_2=language_two,
                file_name=deck_title
                )
            pdf_lesson.format_content()
    # if a file named f"{deck_title}.apkg" exists, in the current folder then show the link to the file 
    if anki_deck:
        st.text("Your deck has been created")            
        st.text("You can download it from the link below")   
        with open(f"{deck_title}.apkg", 'rb') as f:
            contents = f.read()
            st.download_button("Download my deck", data=contents, file_name=f"{deck_title}.apkg")
            # wait for one minute before deleting the audio files
            time.sleep(60)
            cleanup()
    if audio_lesson:
        st.text("Your audio lesson has been created")            
        st.text("You can download it from the link below")   
        with open(f"{deck_title}.mp3", 'rb') as f:
            contents = f.read()
            st.download_button("Download my audio lesson", data=contents, file_name=f"{deck_title}.mp3")
            # wait for one minute before deleting the audio files
            time.sleep(60)
            ttss.delete_audio_files()
    if pdf_lesson:
        st.text("Your pdf lesson has been created")            
        st.text("You can download it from the link below")   
        with open(f"{deck_title}.pdf", 'rb') as f:
            contents = f.read()
            st.download_button("Download my pdf lesson", data=contents, file_name=f"{deck_title}.pdf")
            # wait for one minute before deleting the audio files
            time.sleep(60)
            pdf_lesson.delete_pdf_file()


if __name__ == '__main__':
    main()