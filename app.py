import streamlit as st
import random
import time
from openai import OpenAI
import fitz  # zamiast PyPDF2
#import langchain_community  # dodano import langchain_community

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

# Dodaj side nav menu i przenieś upload PDF do sidebara
with st.sidebar:
    st.header("Menu")
    uploaded_files = st.file_uploader("Wgraj pliki PDF", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                num_pages = pdf_doc.page_count
                # Pobierz tekst z pierwszej strony
                if num_pages > 0:
                    first_page = pdf_doc.load_page(0)
                    text = first_page.get_text()
                else:
                    text = "Brak stron w pliku."
                # Wyświetl nazwę pliku z podglądem w tooltip (popup na hover)
                st.markdown(
                    f'<span title="{text.replace(chr(34), chr(39)).replace(chr(10), " ")}">{uploaded_file.name}</span> '
                    f'({num_pages} stron)', 
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Błąd podczas przetwarzania pliku {uploaded_file.name}: {e}")
