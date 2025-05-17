import streamlit as st
import random
import time
from pdf_utils import extract_pdf_info  # import logiki biznesowej
from ai_model import get_ai_response    # import obsługi modelu AI

st.write("Streamlit loves LLMs! 🤖 [Build your own chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) in minutes, then make it powerful by adding images, dataframes, or even input widgets to the chat.")

st.caption("Note that this demo app isn't actually connected to any LLMs. Those are expensive ;)")



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
        for i in range(5):
            message_placeholder.markdown("Thinking" + "." * (i % 4))
            time.sleep(0.5)

        # Użyj wydzielonej funkcji do uzyskania odpowiedzi AI
        full_response = get_ai_response(st.session_state.messages, st.secrets)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Dodaj side nav menu i przenieś upload PDF do sidebara
with st.sidebar:
    st.header("Menu")
    uploaded_files = st.file_uploader("Wgraj pliki PDF", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        if "dialog_open" not in st.session_state:
            st.session_state.dialog_open = None
        file_infos = []
        for idx, uploaded_file in enumerate(uploaded_files):
            try:
                info = extract_pdf_info(uploaded_file)
                info["idx"] = idx
                file_infos.append(info)
                st.write(f"{info['name']} ({info['num_pages']} stron)")
                if st.button(f"Podgląd", key=f"preview_{idx}"):
                    st.session_state.dialog_open = idx
            except Exception as e:
                st.error(f"Błąd podczas przetwarzania pliku {uploaded_file.name}: {e}")

        # Wyświetl okno dialogowe jeśli wybrano plik do podglądu
        if st.session_state.dialog_open is not None:
            info = file_infos[st.session_state.dialog_open]
            st.markdown(f"### Podgląd: {info['name']}")
            st.markdown(f"**Liczba stron:** {info['num_pages']}")
            st.markdown("---")
            st.markdown("**Tekst z pierwszej strony:**")
            st.markdown(f"<div style='white-space: pre-wrap'>{info['text'] if info['text'] else 'Brak tekstu na pierwszej stronie.'}</div>", unsafe_allow_html=True)
            if st.button("Zamknij podgląd", key="close_dialog"):
                st.session_state.dialog_open = None
