import time
import os
from ollama import Client, Options
import httpx
from ollama import list
from ollama import ListResponse
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PIL import Image
import io
from .api_handler import _Request

# response: ListResponse = list()

from dotenv import load_dotenv

ollama_endpoint = os.environ.get("OLLAMA_ENDPOINT", default="")
chroma_endpoint = os.environ.get("CHROMA_HOST", default="")
client = Client(host=ollama_endpoint, headers={"x-some-header": "some-value"})


def get_image_bytes(image_file):
    image_path = image_file
    image = Image.open(image_path)

    with io.BytesIO() as output:
        image.save(output, format="png")
        image_bytes = output.getvalue()

    return image_bytes


def analyze_image_file(image_file, model, user_prompt):
    # gets image bytes using helper function
    image_bytes = get_image_bytes(image_file)

    stream = client.generate(
        model=model, prompt=user_prompt, images=[image_bytes], stream=True
    )

    return stream


def pdf_to_bytes(_file):
    with open(_file, "rb") as pdf_file:
        pdf_data = pdf_file.read()
    return pdf_data


def ollama_send(llm, prompt, max_len, temperature, top_p, pre_prompt):
    options = Options()
    options.top_p = float(top_p)
    options.temperature = float(temperature)
    options.num_ctx = int(max_len)
    response = client.chat(
        model=llm,
        messages=[
            {"role": "system", "content": pre_prompt},
            {
                "role": "user",
                "content": prompt,
            },
        ],
        options=options,
        stream=True,
    )
    return response


def get_models():
    try:
        response: ListResponse = client.list()
    except:
        response = client.list()

    return response


# Initialize debounce variables
last_call_time = 0
debounce_interval = 2  # Set the debounce interval (in seconds) to your desired value


async def get_all_collection(vectordb):
    uri = "/get_collections"
    if vectordb == "ChromaDB":
        try:
            with httpx.Client() as client:
                response = client.get(chroma_endpoint + uri)
                return response.json()
                # return [doc["name"] for doc in data]
        except Exception as e:
            return e


async def get_elastic_indices():
    uri = "/get_collections"
    async with _Request() as req:
        indices = await req.get(endpoint="http://elastic_api:8000/insert" + uri)
        return indices


def get_collection_details(collection_name, collection_list):
    for doc in collection_list:
        if doc["name"] == collection_name:
            return doc  # Return the dictionary
    return None  # or raise an exception if not found


def debounce_replicate_run(llm, prompt, max_len, temperature, top_p, API_TOKEN):
    global last_call_time
    print("last call time: ", last_call_time)

    # Get the current time
    current_time = time.time()

    # Calculate the time elapsed since the last call
    elapsed_time = current_time - last_call_time

    # Check if the elapsed time is less than the debounce interval
    if elapsed_time < debounce_interval:
        print("Debouncing")
        return "Hello! You are sending requests too fast. Please wait a few seconds before sending another request."

    # Update the last call time to the current time
    last_call_time = time.time()

    # llm, input={"prompt": prompt + "Assistant: ", "max_length": max_len, "temperature": temperature, "top_p": top_p, "repetition_penalty": 1}, api_token=API_TOKEN
    # return output


def get_RCTS_chunks(text, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(text)
    return chunks
