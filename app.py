import streamlit as st
import random
import time
from pdf_utils import extract_pdf_info
from chat_openrouter import ChatOpenRouter
from embedder import *  # zakładamy, że FAISSIndex jest w embedder.py
from ai_model import answer_question

st.write("Streamlit loves LLMs! 🤖 [Build your own chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) in minutes, then make it powerful by adding images, dataframes, or even input widgets to the chat.")

st.caption("Note that this demo app isn't actually connected to any LLMs. Those are expensive ;)")


# Zainicjuj globalną listę plików w session_state
if "files" not in st.session_state:
    st.session_state.files = None

file_infos = []
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        st.write("Thinking...")

        chat = ChatOpenRouter(
            model_name=st.secrets["MODEL"],
        )

        st.write("Retrieving documents...", st.session_state.files)
        if st.session_state.files:
            data = []
            for uploaded_file in st.session_state.files:
                try:
                    info = extract_pdf_info(uploaded_file)
                    data.append(info)
                except Exception as e:
                    st.error(f"Błąd podczas przetwarzania pliku {uploaded_file.name}: {e}")

            index = create_index(file_infos)
            retrieved_docs = retrieve_docs(prompt, index)
            context = "\n\n".join([doc["text"] for doc in retrieved_docs if doc.get("text")])

            template = """
                    You are a helpful assistant. Answer the question based on the context provided. Answer in Polish by default.
                    If the question is not answerable based on the context, say "I don't know".
                    Context: {context}
                    Question: {prompt}
                    Answer:
                """
            print(f"Retrieved documents: {retrieved_docs}")
            st.write("Retrieving documents...")

            response = answer_question(prompt, retrieved_docs, chat, template)     
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(f"Assistant: {response}")
            st.write(response)

        else:
           st.write("No files uploaded. Please upload PDF files to retrieve information.")

with st.sidebar:
    st.header("Menu")
    files = st.file_uploader("Wgraj pliki PDF", type=["pdf"], accept_multiple_files=True)
    if files:
        st.session_state.files = files  # zapisz pliki globalnie
        if "dialog_open" not in st.session_state:
            st.session_state.dialog_open = None

        for idx, uploaded_file in enumerate(files):
            try:
                info = extract_pdf_info(uploaded_file)
                file_infos.append(info)
                st.write(f"{info['filename']}")
                if st.button(f"Podgląd", key=f"preview_{idx}"):
                    st.session_state.dialog_open = idx
            except Exception as e:
                st.error(f"Błąd podczas przetwarzania pliku {uploaded_file.name}: {e}")

        if st.session_state.dialog_open is not None:
            info = file_infos[st.session_state.dialog_open]
            st.markdown(f"### Podgląd: {info['filename']}")
            st.markdown("---")
            st.markdown("**Tekst z pierwszej strony:**")
            st.markdown(f"<div style='white-space: pre-wrap'>{info['text'] if info['text'] else 'Brak tekstu na pierwszej stronie.'}</div>", unsafe_allow_html=True)
            if st.button("Zamknij podgląd", key="close_dialog"):
                st.session_state.dialog_open = None





