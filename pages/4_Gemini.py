import streamlit as st
from utils import get_models
import vertexAI as vt

st.set_page_config(page_title="Gemini Chat", layout="wide")

st.title("Gemini")
PRE_PROMPT = ""
chat_col, upload_col = st.columns([2, 1])
NEW_P = st.sidebar.text_area(
    "Prompt before the chat starts. Edit here if desired:", PRE_PROMPT, height=70
)
if "chat_dialogue" not in st.session_state:
    st.session_state["chat_dialogue"] = []

if NEW_P != PRE_PROMPT and NEW_P != "" and NEW_P != None:
    st.session_state["pre_prompt"] = NEW_P + "\n\n"
else:
    st.session_state["pre_prompt"] = PRE_PROMPT


with upload_col:
    st.container()
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        pdf_content = vt.create_my_data_part(uploaded_file)  # list


with chat_col:
    st.container()
    model_list = vt.get_models()
    # model_names = [model.model for model in model_list.models]
    with st.sidebar:
        image_model = st.selectbox(
            "Which image model would you like to use?", model_list
        )
    for message in st.session_state.chat_dialogue:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # chat Input
    if chat_input := st.chat_input("What would you like to ask?"):
        st.session_state.chat_dialogue.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            string_dialogue = st.session_state["pre_prompt"]
            for dict_message in st.session_state.chat_dialogue:
                if dict_message["role"] == "user":
                    string_dialogue = (
                        string_dialogue + "User: " + dict_message["content"] + "\n\n"
                    )
                else:
                    string_dialogue = (
                        string_dialogue
                        + "Assistant: "
                        + dict_message["content"]
                        + "\n\n"
                    )
        gemini_helper = vt.vertexModel()
        output = gemini_helper.chat_async()
