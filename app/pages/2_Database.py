import streamlit as st
import PyPDF2
from utils.utils import (
    get_models,
    get_all_collection,
    get_elastic_indices,
    get_collection_details,
    get_RCTS_chunks,
)
import asyncio
import pprint


def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    content = ""
    for page_num in range(min(1, num_pages)):
        content += pdf_reader.pages[page_num].extract_text()
    return content


st.set_page_config(page_title="Database", layout="wide")

st.title("Database")
upload_col, db_col = st.columns([2, 1])


with upload_col:
    # File upload
    st.container()
    file = st.file_uploader("Upload a PDF file", type="pdf")
    chunk_size = st.sidebar.slider(
        "Select chunk size", min_value=50, max_value=1000, value=100, step=50
    )
    chunk_overlap = st.sidebar.slider(
        "Select chunk overlap", min_value=0, max_value=100, value=20, step=10
    )
    num_chunks = st.sidebar.number_input(
        "Number of chunks to display", min_value=1, max_value=20, value=5, step=1
    )
    if file is not None:
        # Read PDF and extract text
        content = read_pdf(file)
        # Display the content
        st.container()
        # st.markdown(content)
        chunks = get_RCTS_chunks(content, chunk_size, chunk_overlap)
        st.subheader("Extracted Text:")
        st.write(
            f"Total Text Chunks:{len(chunks)}",
            chunks[:num_chunks],
            unsafe_allow_html=True,
        )
        if st.button("Upload chunks to selected index"):
            progress_bar = st.progress(0)
            status = st.empty()

        # from utils.utils import (
        #     get_embedding_function,
        #     upload_chunk_to_es,
        # )  # you implement these

        # embed_model = st.session_state["embedding_model"]
        # index_name = st.session_state["collection"]

        # embedding_fn = get_embedding_function(embed_model)  # returns a callable
        # total_chunks = len(chunks)

        # for i, chunk in enumerate(chunks):
        #     embedding = embedding_fn(chunk)

        #     doc = {
        #         "text": chunk,
        #         "embedding": embedding,
        #         "chunk_id": i,
        #         "source": file.name,
        #     }

        #     # upload_chunk_to_es(index=index_name, doc=doc)

        #     progress = (i + 1) / total_chunks
        #     progress_bar.progress(progress)
        #     status.text(f"Uploaded chunk {i + 1}/{total_chunks}")

        # status.success(f"All {total_chunks} chunks uploaded to '{index_name}'!")

with db_col:
    response = get_models()
    model_list = [model.model for model in response.models if "embed" in model.model]

    vector_db = st.selectbox(
        "VectorDB",
        ["Elasticsearch", "ChromaDB"],
        key="vectordb",
    )
    selected_option = st.selectbox("Choose a Embedding model:", model_list, key="model")
    st.session_state["embedding_model"] = selected_option
    if st.session_state["vectordb"] == "Elasticsearch":
        collection_list = asyncio.run(get_elastic_indices())
    else:
        pass
    try:
        names = [doc["name"] for doc in collection_list]
    except:
        names = []
    db_option = st.selectbox("Choose a Collection:", names, key="collection")
    if db_option:
        details_dict = get_collection_details(db_option, collection_list)
        pretty_details = pprint.pformat(details_dict)
        st.markdown(
            f"""
                <style>
                .stCode {{
                    max-width: 95%;
                }}
                </style>
                """,
            unsafe_allow_html=True,
        )
        st.code(pretty_details, language="python")  # Alternative: display as code block
