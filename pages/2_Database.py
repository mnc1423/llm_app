import streamlit as st
import PyPDF2
from utils import get_models, get_all_collection, get_collection_details
import pprint


def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    content = ""
    for page_num in range(min(1, num_pages)):
        content += pdf_reader.pages[page_num].extract_text()
    return content


st.title("Database")

upload_col, db_col = st.columns([2, 1])


with upload_col:
    # File upload
    st.container()
    file = st.file_uploader("Upload a PDF file", type="pdf")

    if file is not None:
        # Read PDF and extract text
        content = read_pdf(file)
        # Display the content
        st.container()
        st.subheader("Extracted Text:")
        st.markdown(content)
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
    names = [doc["name"] for doc in collection_list]
    db_option = st.selectbox("Choose a Collection:", names, key="collection")
    if db_option:
        details_dict = get_collection_details(db_option, collection_list)
        pretty_details = pprint.pformat(details_dict)

        # Display using st.text_area() (or st.code() for code block)
        # st.text_area("Collection Details", pretty_details, height=250)
        st.code(pretty_details, language="python")  # Alternative: display as code block
