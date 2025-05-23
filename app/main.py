import streamlit as st
from dotenv import load_dotenv


load_dotenv()
import os
from utils.utils import ollama_send, get_models

###Initial UI configuration:###
st.set_page_config(page_title="LLM Chat App", page_icon="🦙", layout="wide")

PRE_PROMPT = ""
OLLAMA_ENDPOINT = os.environ.get("OLLAMA_ENDPOINT", default="")


def render_app():

    # reduce font sizes for input text boxes
    custom_css = """
        <style>
            .stTextArea textarea {font-size: 13px;}
            div[data-baseweb="select"] > div {font-size: 13px !important;}
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Left sidebar menu
    st.sidebar.header("Chat Options")
    # Set config for a cleaner menu, footer & background:
    hide_streamlit_style = """
                <style>
                # MainMenu {visibility: ;}
                footer {visibility: ;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # container for the chat history
    response_container = st.container()
    # container for the user's text input
    container = st.container()
    # Set up/Initialize Session State variables:
    st.session_state["user_info"] = "test"
    if "chat_dialogue" not in st.session_state:
        st.session_state["chat_dialogue"] = []
    if "llm" not in st.session_state:
        # st.session_state['llm'] = REPLICATE_MODEL_ENDPOINT13B
        st.session_state["llm"] = OLLAMA_ENDPOINT
    if "temperature" not in st.session_state:
        st.session_state["temperature"] = 0.1
    if "top_p" not in st.session_state:
        st.session_state["top_p"] = 0.9
    if "max_seq_len" not in st.session_state:
        st.session_state["max_seq_len"] = 512
    if "pre_prompt" not in st.session_state:
        st.session_state["pre_prompt"] = PRE_PROMPT
    if "string_dialogue" not in st.session_state:
        st.session_state["string_dialogue"] = ""

    # Dropdown menu to select the model edpoint:
    response = get_models()
    model_list = []
    for model in response.models:
        if "embed" in model.model:
            continue
        else:
            model_list.append(model.model)
    selected_option = st.sidebar.selectbox(
        "Choose a LLM model:", model_list, key="model"
    )
    st.session_state["llm"] = selected_option
    st.session_state["temperature"] = st.sidebar.slider(
        "Temperature:", min_value=0.01, max_value=5.0, value=0.1, step=0.01
    )
    st.session_state["top_p"] = st.sidebar.slider(
        "Top P:", min_value=0.01, max_value=1.0, value=0.9, step=0.01
    )
    st.session_state["max_seq_len"] = st.sidebar.slider(
        "Max Sequence Length:", min_value=64, max_value=4096, value=2048, step=8
    )

    NEW_P = st.sidebar.text_area(
        "Prompt before the chat starts. Edit here if desired:", PRE_PROMPT, height=70
    )
    if NEW_P != PRE_PROMPT and NEW_P != "" and NEW_P != None:
        st.session_state["pre_prompt"] = NEW_P + "\n\n"
    else:
        st.session_state["pre_prompt"] = PRE_PROMPT

    btn_col1, btn_col2 = st.sidebar.columns(2)

    # Add the "Clear Chat History" button to the sidebar
    def clear_history():
        st.session_state["chat_dialogue"] = []

    clear_chat_history_button = btn_col1.button(
        "Clear History", use_container_width=True, on_click=clear_history
    )

    st.sidebar.header("Tools")
    tool_option = st.sidebar.multiselect("Choose Tool:", model_list, key="tools")

    # Display chat messages from history on app rerun
    for message in st.session_state.chat_dialogue:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Type your question here to talk to LLaMA2"):
        # Add user message to chat history
        st.session_state.chat_dialogue.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

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
            output = ollama_send(
                st.session_state["llm"],
                string_dialogue + "Assistant: ",
                st.session_state["max_seq_len"],
                st.session_state["temperature"],
                st.session_state["top_p"],
                st.session_state["pre_prompt"],
            )
            try:
                for item in output:
                    full_response += item["message"]["content"]
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            except:
                pass
        # Add assistant response to chat history
        st.session_state.chat_dialogue.append(
            {"role": "assistant", "content": full_response}
        )


# if "user_info" in st.session_state:
# if user_info:
render_app()
# else:
# st.write(
#     "Please login to use the app. This is just to prevent abuse, we're not charging for usage."
# )
# st.session_state["user_info"] = login_button(AUTH0_CLIENTID, domain=AUTH0_DOMAIN)
