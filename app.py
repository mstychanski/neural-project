import streamlit as st
import random
import time
from openai import OpenAI
from PyPDF2 import PdfReader  # Dodano do obsługi PDF

st.write("Streamlit loves LLMs! 🤖 [Build your own chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) in minutes, then make it powerful by adding images, dataframes, or even input widgets to the chat.")

st.caption("Note that this demo app isn't actually connected to any LLMs. Those are expensive ;)")



client = OpenAI(api_key = st.secrets["API_KEY"], base_url=st.secrets["BASE_URL"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

 # Show waiting dots animation
        for i in range(5):  # Adjust the range for longer/shorter animations
            message_placeholder.markdown("Thinking" + "." * (i % 4))
            time.sleep(0.5)

        assistant_response = client.chat.completions.create(
            model=st.secrets["MODEL"],
            messages=st.session_state.messages
        )
        full_response = assistant_response.choices[0].message.content
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Dodaj przycisk do uploadowania pliku PDF
uploaded_file = st.file_uploader("Wgraj plik PDF", type=["pdf"])
if uploaded_file is not None:
    try:
        pdf_reader = PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)
        st.success(f"Plik PDF został wczytany. Liczba stron: {num_pages}")
        # Przykładowo: wyświetl tekst z pierwszej strony
        if num_pages > 0:
            first_page = pdf_reader.pages[0]
            text = first_page.extract_text()
            st.write("Tekst z pierwszej strony:")
            st.write(text if text else "Brak tekstu na pierwszej stronie.")
    except Exception as e:
        st.error(f"Błąd podczas przetwarzania pliku PDF: {e}")
