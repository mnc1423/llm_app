import streamlit as st
import time
import numpy as np
from utils.utils import (
    get_models,
    get_elastic_indices,
    ollama_embedding,
    init_session_state,
)
import asyncio

rag_default = {
    "embedding_model": "",
    "chat_dialogue": [],
    "string_dialogue": "",
    "model": "",
}

st.set_page_config(page_title="RAG Chat", layout="wide")
chat_col, doc_col = st.columns([2, 1])

# init
if "embedding_model" not in st.session_state:
    st.session_state["embedding_model"] = None

# side bar config
st.sidebar.selectbox("Vector DB", ["Elasticsearch", "ChromaDB"], key="vectordb")
response = get_models()
model_list = [model.model for model in response.models if "embed" in model.model]
selected_option = st.sidebar.selectbox(
    "Choose a Embedding model:", model_list, key="model"
)
if st.session_state["vectordb"] == "Elasticsearch":
    collection_list = asyncio.run(get_elastic_indices())
names = [doc["name"] for doc in collection_list]


db_options = st.sidebar.selectbox("Choose a Collection", names, key="collections")

st.session_state["k_docs"] = st.sidebar.slider(
    "Number of docs", min_value=1, max_value=20, value=5, step=1
)

# create Chat
with doc_col:
    st.container()
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
        else:
            # append the latest history
        # for item in output:
        #     full_response += item.text
        #     message_placeholder.markdown(full_response + "▌")
        # message_placeholder.markdown(full_response)

with chat_col:
    st.container()
