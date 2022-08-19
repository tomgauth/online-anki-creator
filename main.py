from tkinter import SEPARATOR
from tkinter.ttk import Separator
import streamlit as st
import genanki
import random
from os.path import exists
import time

SEPARATOR = ";"

def gen_anki_id():
    return random.randrange(1 << 30, 1 << 31)


my_model = genanki.Model(
  gen_anki_id(),
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])


# Create a function that will take some input from streamlit (st.text_input) and return it back to the user (st.write)


def txt_to_list_of_lists(text_input):
    table = [line.split(SEPARATOR) for line in text_input.split("\n")]
    # remove any empty lines
    table = [line for line in table if line != ['']]
    return table





def to_anki_deck(table, deck_title):
    my_deck = genanki.Deck(gen_anki_id(), deck_title)
    package = genanki.Package(my_deck) 
    i = 0
    my_bar = st.progress(i)       
    for row in table:
        my_bar.progress(i/len(table))
        try:
            note = genanki.Note(
                    model = my_model,
                    fields = [row[0], row[1]]
                )
        except IndexError:
            pass
        my_deck.add_note(note)
    package.write_to_file(f"{deck_title}.apkg")
    return f"{deck_title}.apkg"


def main():    
    anki_deck = None
    with st.form("input phrases"):
        st.title("Create your Anki Deck below!")
        st.text("This is a simple text input, use ; to separate the fields")
        content = st.text_area("Write your list of phrases")
        table = txt_to_list_of_lists(content)
        deck_title = title = st.text_input("Deck Title")
        submitted = st.form_submit_button("Submit")
        # st.write(table)
        if submitted:
            anki_deck = to_anki_deck(table, deck_title)   
            st.text("Your deck has been created")            
            st.text("You can download it from the link below")            
    # if a file named f"{deck_title}.apkg" exists, in the current folder then show the link to the file 
    if anki_deck:
        with open(f"{deck_title}.apkg", 'rb') as f:
            contents = f.read()
            st.download_button("Download my deck", data=contents, file_name=f"{deck_title}.apkg")   

if __name__ == '__main__':
    main()