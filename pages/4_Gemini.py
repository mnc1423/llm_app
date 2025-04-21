from google.oauth2 import service_account
from google_modules.vertexAI import VertexAI
import streamlit as st

# credentials = service_account.Credentials.from_service_account_file()


st.set_page_config(page_title="Gemini", layout="wide")

st.title("Gemini")
chat_col, model_col = st.columns([2, 1])

gemini = VertexAI()

st.sidebar.header("Chat Options")


gemini_list = gemini.get_gemini_models()

selected_option = st.sidebar.selectbox(
    "Choose a Gemini model:", gemini_list, key="model"
)
message_placeholder = st.empty()
if "string_dialogue" not in st.session_state:
    st.session_state["string_dialogue"] = ""

if "chat_dialogue" not in st.session_state:
    st.session_state["chat_dialogue"] = []
container = st.container()
response_container = st.container()


# display chat messages from history on app rerun
for message in st.session_state.chat_dialogue:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Type your question here to talk to Gemini"):

    st.session_state.chat_dialogue.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("model"):
        message_placeholder = st.empty()

        full_response = ""
        gemini_model = st.session_state["model"]
        string_dialogue = ""
        for dict_message in st.session_state.chat_dialogue:
            if dict_message["role"] == "user":
                string_dialogue = (
                    string_dialogue + "User: " + dict_message["content"] + "\n\n"
                )
            else:
                string_dialogue = (
                    string_dialogue + "Assistant: " + dict_message["content"] + "\n\n"
                )
        output = gemini.generate_streaming(
            model=gemini_list[gemini_model], content=prompt
        )
        try:
            for item in output:
                full_response += item.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except:

            pass
    st.session_state.chat_dialogue.append({"role": "model", "content": full_response})
