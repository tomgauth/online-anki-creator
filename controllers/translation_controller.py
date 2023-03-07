import deepl 
import streamlit as st
import os
# get the api key from the file api_key_deepl.txt

if "api_key_deepl.txt" in os.listdir():
    with open("api_key_deepl.txt", "r") as f:
        auth_key = f.read()
else:
    auth_key = st.text_input("Deepl API key", type="password")


class TranslationController:
    def __init__(self, text, target_language, formality="prefer_less"):
        self.text = text
        self.target_language = target_language
        self.formality = formality
        self.translated_text = ""
        self.translator = deepl.Translator(auth_key)
        
    def translate(self):
        # returns a translation of the text in the target language
        result = self.translator.translate_text(self.text, target_lang=self.target_language) 
        self.translated_text = result.text
        return self.translated_text

    def multi_line(self):
        # translates the multi-line text and returns a multi-line text with the translation of each line, separated by a semicolon
        # remove any empty lines
        lines = self.text.splitlines()
        lines = [line for line in self.text.splitlines() if line.strip() != ""]        
        translated_lines = []
        for line in lines:
            translation = self.translator.translate_text(line, target_lang=self.target_language).text
            translated_lines.append(line + " ; " + translation )            
        # convert the list of translated lines into a multi-line string by joining the list with a newline character
        self.translated_text = "\n".join(translated_lines)
        return self.translated_text
        

# from controllers.translation_controller import *
def test_translate_text():
    # test the translation of a single line of text
    text = """
    Essayer quelque chose de nouveau
je m'en fous
vous n'êtes pas d'accord
tu fais quoi, là?
Parler un petit peu de ma vie
Faire des phrases courtes
Ne pas savoir ce que je vais faire
Aimer bien manger une pizza
Ne pas savoir trop
Ne pas avoir faim
Ne pas avoir de plan
Vouloir faire des choses
Vouloir profiter de la vie
Essayer de nouvelles choses
Écouter ses envies
Écouter son corps
Prendre des décisions
Dire ce qu'on pense"""
    target_language = "DE"
    translator = TranslationController(text, target_language)
    translation = translator.multi_line()
    print(translation)
