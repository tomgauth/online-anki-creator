import os
import time
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from models.lesson import Lesson
# from controllers.ai_transcriber import AiTrancriber
from controllers.generate_anki_deck import AnkiDeckGenerator
from controllers.generate_pdf_lesson import PDFLessonGenerator
from controllers.generate_audio_lesson import AudioLessonGenerator
from services.translator import Translator
import genanki
from models.anki_model import gen_anki_id, anki_template
from services.cleaner import Cleaner
from services.text_to_speech import TextToSpeech
from services.speech_to_text import AiTrancriber
from services.sentence_formatter import AiFormatter

GOOGLE_LANGUAGES = ['af', 'ar', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'en-au', 'en-uk', 'en-us', 'eo', 'es', 'es-es', 'es-us', 'fi', 'fr', 'hi', 'hr', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'ko', 'la', 'lv', 'mk', 'nl', 'no', 'pl', 'pt', 'pt-br', 'ro', 'ru', 'sk', 'sq', 'sr', 'sv', 'sw', 'ta', 'th', 'tr', 'vi', 'zh', 'zh-cn', 'zh-tw', 'zh-yue']

DEEPL_LANGUAGES = ['BG', 'CS', 'DA', 'DE', 'EL', 'EN-GB', 'EN-US', 'ES', 'ET', 'FI', 'FR', 'HU', 'ID', 'IT', 'JA', 'KO', 'LT', 'LV', 'NB', 'NL', 'PL', 'PT-BR', 'PT-PT', 'RO', 'RU', 'SK', 'SL', 'SV', 'TR', 'UK', 'ZH']

SEPARATOR = ";"

def main():
    
    with st.form("form"):
        col1, col2 = st.columns(2)
        with col1:
            origin_language = st.selectbox("Select the origin language", DEEPL_LANGUAGES, index=10)            
        with col2:        
            target_language = st.selectbox("Select the target language", DEEPL_LANGUAGES, index=5)
        
        
        # audio_bytes = audio_recorder("Record a list of sentences")        

        ai_generated_phrases = None
        audio_upload = st.file_uploader("Upload an audio file", type=["mp3"], accept_multiple_files=False)
        # rename the audio file to audio.mp3
        if audio_upload:
            st.write("audio uploaded")
            with open("uploaded_audio.mp3", "wb") as f:
                f.write(audio_upload.read())

        audio_bytes = audio_recorder()
        st.audio(audio_bytes, format="audio/mp3")

        # the following if statement
        if audio_bytes:
            with open("recorded_audio.mp3", "wb") as f:
                f.write(audio_bytes)
        # add a button to delete the auddio file
        if st.checkbox("Delete audio file"):
            if "recorded_audio.mp3" in os.listdir() or "uploaded_audio.mp3" in os.listdir():
                os.remove("recorded_audio.mp3")
                os.remove("uploaded_audio.mp3")
            if audio_bytes:
                audio_bytes = None

        if st.checkbox("Use Recording"):
            # use the lastest audio file
            # convert audio_bytes to audio.mp3
            audio_file = audio_bytes
            # audio_upload if audio_upload else audio_bytes
            if "recorded_audio.mp3" in os.listdir():
                print("---> audio.mp3 exists")                     
                transcriber = AiTrancriber("recorded_audio.mp3", target_language)
                print("---> transcriber", transcriber)
                transcript = transcriber.transcribe()
                print("---> transcript", transcript)
                formatter = AiFormatter(transcript.text)
                phrases = formatter.format_phrases()
                translator = Translator(phrases, target_language)
                ai_generated_phrases = translator.multi_line() 
                print("---> ai generated phrases", ai_generated_phrases)
        
        if st.checkbox("Use Upload"):
            audio_file = audio_upload
            if "uploaded_audio.mp3" in os.listdir():
                transcriber = AiTrancriber("uploaded_audio.mp3", target_language)
                transcript = transcriber.transcribe()
                formatter = AiFormatter(transcript.text)
                phrases = formatter.format_phrases()
                translator = Translator(phrases, target_language)
                ai_generated_phrases = translator.multi_line() 
    
        
        lesson_name = st.text_input("Enter a name for the lesson", value="Default Lesson Name")

        generate_anki_deck = st.form_submit_button("Generate Anki deck")
        generate_pdf = st.form_submit_button("Generate PDF")
        generate_audio_lesson = st.form_submit_button("Generate audio lesson")
    
        # input information for the audio lesson
        if ai_generated_phrases:
            # prefill the form with the generated phrases
            content = st.text_area(label= "input your vocabulary" , value=ai_generated_phrases ,placeholder="""hello ; bonjour
    thank you ; merci""", height=200)
        else:            
            content = st.text_area(label= "input your vocabulary" , placeholder="""hello ; bonjour
    thank you ; merci""", height=200)
        col1, col2 = st.columns(2)
        with col1:
            intro = st.text_area(label= "input your intro" ,placeholder="Lesson 1", height=20)
            outro = st.text_area(label= "input your outro" ,placeholder="Thank you for listening", height=20)
        with col2:
            silence_between_blocks_duration = st.number_input("Silence between blocks duration", min_value=0, max_value=10, value=1)
            silence_between_phrases_duration = st.number_input("Silence between phrases duration", min_value=0, max_value=10, value=2)
            silence_between_repeat = st.number_input("Silence between repeat", min_value=0, max_value=10, value=1)
            repeat_origin_phrase = st.number_input("Repeat origin phrase", min_value=0, max_value=10, value=1)
            repeat_target_phrase = st.number_input("Repeat target phrase", min_value=0, max_value=10, value=1)
            block_type = st.selectbox("Block Type", ["recall", "repeat", "recognize"])
            shuffle_blocks = st.checkbox("Shuffle Blocks")
        

        lesson = Lesson(
                lesson_name=lesson_name,
                origin_language=origin_language,
                target_language=target_language,
                content=content,
                intro=intro,
                outro=outro
            )
        read_intro = True if intro else False
        read_outro = True if outro else False
        
        st.write("Lesson", lesson)
        st.write("Lesson content", lesson.content)
        
    if generate_anki_deck:
        st.write(content)
        params = {
            "audio": True,
        }
        
        anki_generator = AnkiDeckGenerator(lesson, anki_template, params)
        deck_name = anki_generator.generate_deck()
        with open(deck_name, 'rb') as f:
            contents = f.read()
            st.download_button("Download my deck", data=contents, file_name=deck_name)
            # wait for one minute before deleting the audio files
            time.sleep(60)
            Cleaner.remove_apkg_files()
            Cleaner.remove_mp3_files()

    if generate_pdf:
        pdf_generator = PDFLessonGenerator(lesson)
        pdf_file = pdf_generator.format_content()
        with open(pdf_file, 'rb') as f:
            contents = f.read()
            st.download_button("Download my Pdf", data=contents, file_name=f'{lesson.lesson_name}.pdf')
            # wait for one minute before deleting the audio files
            time.sleep(60)
            Cleaner.remove_pdf_files()
        

    if generate_audio_lesson:
        params={
            "silence_between_blocks_duration": silence_between_blocks_duration,
            "silence_between_repeat": silence_between_repeat,
            "silence_between_phrases_duration": silence_between_phrases_duration,
            "repeat_1": repeat_origin_phrase,
            "repeat_2": repeat_target_phrase,
            "block_type": block_type,
            "shuffle_blocks": shuffle_blocks,
            "read_intro": read_intro,
            "read_outro": read_outro                

        }
        audio_generator = AudioLessonGenerator(lesson, params)
        audio_lesson = audio_generator.generate_audio_lesson()

        with open(audio_lesson, 'rb') as f:
            contents = f.read()
            st.download_button("Download my Audio Lesson", data=contents, file_name=f'{lesson.lesson_name}.mp3')
            # wait for one minute before deleting the audio files
            st.success("Audio Lesson generated successfully!")
            time.sleep(60)            
            Cleaner.remove_mp3_files()
            

        # Display success message



if __name__ == "__main__":
    main()