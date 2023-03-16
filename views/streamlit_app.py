import os
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from models.lesson import Lesson
from controllers.ai_transcriber import AiTrancriber


google_language_list = ['af', 'sq', 'ar', 'hy', 'bn', 'ca', 'zh', 'zh-cn', 'zh-tw', 'zh-yue', 'hr', 'cs', 'da', 'nl', 'en', 'en-au', 'en-uk', 'en-us', 'eo', 'fi', 'fr', 'de', 'el', 'hi', 'hu', 'is', 'id', 'it', 'ja', 'ko', 'la', 'lv', 'mk', 'no', 'pl', 'pt', 'pt-br', 'ro', 'ru', 'sr', 'sk', 'es', 'es-es', 'es-us', 'sw', 'sv', 'ta', 'th', 'tr', 'vi', 'cy']

language_list_deepl = ["BG","CS","DA","DE","EL","EN-GB","EN-US","ES","ET","FI","FR","HU","ID","IT","JA","KO","LT","LV","NB","NL","PL","PT-BR","PT-PT","RO","RU","SK","SL","SV","TR","UK","ZH"]



# chatgpt golfing the shit out of these two lists

def generate_phrases(audio_bytes, recording_file, target_language):
    if audio_bytes or recording_file:
        # use the lastest audio file
        # convert audio_bytes to audio.mp3
        audio_file = audio_bytes or recording_file
        # audio_upload if audio_upload else audio_bytes
        st.audio(audio_file, format="audio/mp3")
    if "audio.mp3" in os.listdir():
        at = AiTrancriber("audio.mp3", target_language)
        ai_generated_phrases = at.format_phrases()
        return ai_generated_phrases
    else:
        return None



def main():
    # a field for uploading an audio file
    # a record button using audio_recorder
    # a field for entering text
    # create 2 columns using st.beta_columns
    recording_file = st.file_uploader("Upload an audio recording")
    audio_bytes = audio_recorder("Record a list of sentences")
    ai_generated_phrases = generate_phrases(audio_bytes, recording_file, target_language)

    with open("audio.mp3", "wb") as f: f.write(audio_bytes) if audio_bytes else None
    col1, col2 = st.columns(2)
    with col1:
        origin_language = st.selectbox("Select the origin language", language_list_deepl, index=6)
    with col2:        
        target_language = st.selectbox("Select the target language", language_list_deepl, index=10)    
    
    lesson_name = st.text_input("Enter a name for the lesson")
   
    # input information for the audio lesson
    if ai_generated_phrases:
        # prefill the form with the generated phrases
        content = st.text_area(label= "input your vocabulary" , value=ai_generated_phrases ,placeholder=ai_generated_phrases, height=200)
    else:            
        content = st.text_area(label= "input your vocabulary" ,placeholder="""hello ; bonjour
thank you ; merci""", height=200)
    col1, col2 = st.columns(2)
    with col1:
        intro = st.text_area(label= "input your intro" ,placeholder="Lesson 1", height=20)
        outro = st.text_area(label= "input your outro" ,placeholder="Thank you for listening", height=20)
    with col2:
        silence_between_blocks_duration = st.number_input("Silence between blocks duration", min_value=0, max_value=10, value=1)
        silence_between_phrases_duration = st.number_input("Silence between phrases duration", min_value=0, max_value=10, value=2)
        block_type = st.selectbox("Block Type", ["recall", "repeat", "recognize"])
        shuffle_blocks = st.checkbox("Shuffle Blocks")
    
    generate_anki_deck = st.checkbox("Generate Anki deck")
    generate_pdf = st.checkbox("Generate PDF")
    generate_audio_lesson = st.checkbox("Generate audio lesson")
        

    if st.button("Generate Lesson"):
        # Create the lesson
        lesson = Lesson()

        # Generate the lesson components
        if generate_anki_deck:
            # anki_deck_controller.generate_anki_deck()
            pass

        if generate_pdf:
            # lesson_controller.generate_pdf()
            pass

        if generate_audio_lesson:
            # lesson_controller.generate_audio_lesson()
            pass

        # Display success message
        st.success("Lesson generated successfully!")

if __name__ == "__main__":
    main()