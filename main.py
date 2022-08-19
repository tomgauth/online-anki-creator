import streamlit as st

# Using Anki create a deck of cards using the language and target language


# Create a function that will take some input from streamlit (st.text_input) and return it back to the user (st.write)
def main():
    st.title("Create your Anki Deck below!")
    st.text("This is a simple text input")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Your language")
        language = st.text_input("Enter your language")
        lang_content = st.text_area("Write your list of phrases")
        st.write(lang_content)

    with col2:
        st.header("Target language")
        target_language = st.text_input("Enter the language you're learning")
        targt_content = st.text_area("Write your list of translated phrases")
        st.write(targt_content)

          

if __name__ == '__main__':
    main()