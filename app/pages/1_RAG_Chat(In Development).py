import streamlit as st
import asyncio
from utils.utils import (
    get_models,
    get_elastic_indices,
    ollama_embedding,
    init_session_state,
    vector_search,
)

rag_default = {
    "embedding_model": "",
    "chat_dialogue": [],
    "string_dialogue": "",
    "model": "",
}

st.set_page_config(page_title="RAG Chat", layout="wide")
chat_col, doc_col = st.columns([2, 1])

# Initialize session state only once
init_session_state(rag_default)

# Sidebar config
st.sidebar.selectbox("Vector DB", ["Elasticsearch", "ChromaDB"], key="vectordb")
response = get_models()
model_list = [model.model for model in response.models if "embed" in model.model]
st.sidebar.selectbox("Choose a Embedding model:", model_list, key="model")

# Get collections
if st.session_state["vectordb"] == "Elasticsearch":
    collection_list = asyncio.run(get_elastic_indices())
else:
    collection_list = []  # Add ChromaDB collection fetch if available
names = [doc["name"] for doc in collection_list]

if names:
    st.sidebar.selectbox("Choose a Collection", names, key="collections")
else:
    st.session_state["collections"] = None

st.sidebar.slider(
    "Number of docs", min_value=1, max_value=20, value=5, step=1, key="k_docs"
)

with doc_col:
    st.markdown("### Retrieved Documents")
    if "retrieved_docs" in st.session_state:
        for i, doc in enumerate(st.session_state["retrieved_docs"]):
            st.markdown(f"**Doc {i+1}:** {doc}")

with chat_col:
    st.markdown("### RAG Chat")
    for msg in st.session_state["chat_dialogue"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Type your question here to talk to Gemini")
    if prompt:
        st.session_state["chat_dialogue"].append({"role": "user", "content": prompt})
        # Embedding
        embedding = ollama_embedding(st.session_state["model"], prompt)
        # Vector Search
        async def do_vector_search():
            return await vector_search(
                st.session_state["vectordb"],
                st.session_state["collections"],
                embedding,
                st.session_state["k_docs"],
            )

        retrieved_docs = asyncio.run(do_vector_search())
        st.session_state["retrieved_docs"] = [doc.get("content", str(doc)) for doc in retrieved_docs]
        # RAG context
        context = "\n\n".join(st.session_state["retrieved_docs"])
        rag_prompt = f"Context:\n{context}\n\nUser: {prompt}\nAssistant:"
        rag_response = f"[LLM response based on context: {context[:100]}... and user query: {prompt}]"
        st.session_state["chat_dialogue"].append({"role": "model", "content": rag_response})
