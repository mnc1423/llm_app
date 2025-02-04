import streamlit as st
import io
import tempfile
from PIL import Image
from utils import get_models, analyze_image_file

st.set_page_config(page_title="Image", layout="wide")

st.title("Image")
upload_col, db_col = st.columns([2, 1])


def create_temp_file(text_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(text_file.getvalue())
        tmp_path = tmp.name

        return tmp_path


# handles stream response back from LLM
def stream_parser(stream):
    for chunk in stream:
        yield chunk["response"]


with upload_col:
    st.container()
    img_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    model_list = get_models()
    model_names = [model.model for model in model_list.models]  #

    with st.sidebar:
        image_model = st.selectbox(
            "Which image model would you like to use?", model_names
        )

    if chat_input := st.chat_input("What would you like to ask?"):
        if img_file is None:
            st.error("You must select an image file to analyze!")
            st.stop()

        with st.status(
            ":red[Processing image file. DON'T LEAVE THIS PAGE WHILE IMAGE FILE IS BEING ANALYZED...]",
            expanded=True,
        ) as status:
            st.write(":orange[Analyzing Image File...]")

            # creates the audio file
            stream = analyze_image_file(
                img_file, model=image_model, user_prompt=chat_input
            )

            stream_output = st.write_stream(stream_parser(stream))

            st.write(":green[Done analyzing image file]")
