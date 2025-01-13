import time
import os
from ollama import Client, Options

from ollama import list
from ollama import ListResponse

# response: ListResponse = list()

from dotenv import load_dotenv

REPLICATE_MODEL_ENDPOINT7B = os.environ.get("REPLICATE_MODEL_ENDPOINT7B", default="")
client = Client(
    host=REPLICATE_MODEL_ENDPOINT7B, headers={"x-some-header": "some-value"}
)


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
    response: ListResponse = client.list()
    return response


# Initialize debounce variables
last_call_time = 0
debounce_interval = 2  # Set the debounce interval (in seconds) to your desired value


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
