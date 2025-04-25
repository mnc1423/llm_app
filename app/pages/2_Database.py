import streamlit as st
import PyPDF2
from utils.utils import (
    get_models,
    get_all_collection,
    get_collection_details,
    get_RCTS_chunks,
)
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
        print(type(content))
        # Display the content
        st.container()
        st.subheader("Extracted Text:")
        # st.markdown(content)
        chunks = get_RCTS_chunks(content, chunk_size, chunk_overlap)
        st.write(
            "Text Chunks:",
            chunks[:num_chunks],
            unsafe_allow_html=True,
        )
with db_col:
    response = get_models()
    model_list = []
    for model in response.models:
        if "embed" in model.model:
            model_list.append(model.model)
        else:
            continue
    selected_option = st.selectbox("Choose a Embedding model:", model_list, key="model")
    st.session_state["llm"] = selected_option
    collection_list = get_all_collection()
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
        # Display using st.text_area() (or st.code() for code block)
        # st.text_area("Collection Details", pretty_details, height=250)
        st.code(pretty_details, language="python")  # Alternative: display as code block
