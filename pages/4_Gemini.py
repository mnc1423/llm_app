from google.oauth2 import service_account
from vertexAI import VertexAI
import streamlit as st

# credentials = service_account.Credentials.from_service_account_file()


st.set_page_config(page_title="Gemini", layout="wide")

st.title("Gemini")
chat_col, model_col = st.columns([2,1])

gemini = VertexAI()

st.sidebar.header("Chat Options")


gemini_list = gemini.get_gemini_models()

selected_option = st.sidebar.selectbox(
        "Choose a Gemini model:", gemini_list, key="model"
)
# with chat_col:
#     st.container()
message_placeholder = st.empty()
if "chat_dialogue" not in st.session_state:
    st.session_state["chat_dialogue"] = []
    container = st.container()
    response_container = st.container()

    if prompt := st.chat_input("Type your question here to talk to Gemini"):
        # Add user message to chat history
        st.session_state.chat_dialogue.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        try:
            for item in output:
                full_response += item["message"]["content"]
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except:
            pass
        st.session_state.chat_dialogue.append(
            {"role": "assistant", "content": full_response}
        )

