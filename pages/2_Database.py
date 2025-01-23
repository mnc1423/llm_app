import streamlit as st
import PyPDF2


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
    pass
