<<<<<<< HEAD
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
API_KEY = os.environ.get("API_KEY", default="")



class VertexAI:
    def __init__(self, vertexAI:bool=False):
        if vertexAI:
            self.client = genai.Client(
                vertexai=True,
                project="",
                location="",
            )
        else:
            self.client = genai.Client(api_key=API_KEY)

    def generate_content(self, model, content):
        self.client.models.generate_content(
            model=model, contents=content
        )

    def get_gemini_models(self):
        gemini_models = []
        for model in self.client.models.list():
            if "gemini" in model.name:
                gemini_models.append(model.display_name)
        return gemini_models



    
=======
from vertexai.generative_models import GenerativeModel, Part, grounding, Content, Tool
import mimetypes


def get_models() -> list[str]:
    models = [
        "gemini-2.0-flash-001",
        "gemini-2.0-lite-preview-02-05",
        "gemini-2.0-pro-exp-02-05",
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-thinking-exp-01-21",
        "gemini-1.5-flash-002",
        "gemini-1.5-pro-002",
    ]
    return models


def create_youtube_part(self, uri: str) -> list[Content]:
    """Creates Content from youtube"""
    video_link = [
        Content(role="user", parts=[Part.from_uri(uri=uri, mime_type="video/*")])
    ]
    return video_link


def create_my_data_part(self, data: bytes) -> list[Content]:
    """Creates Content from data"""
    loaded_data = []
    loaded_data.append(
        Content(
            role="user",
            parts=[Part.from_data(data=data, mime_type="application/pdf")],
        )
    )
    return loaded_data


class vertexModel:
    def __init__(self, yt_link: str):
        self.llm_model = self.create_llm_model()
        self.loaded_data = []
        self.contents = []  # Test Needed

    def create_llm_model(self, tools=None, tools_config=None):
        llm_model = GenerativeModel(
            model_name=self.llm_model,
            generation_config=self.gen_settings,
            system_instruction=self.chat_settings["command"],
            tools=tools,
            tool_config=tools_config,
        )
        return llm_model

    def chat_async(
        self,
        # my_llm_model: GenerativeModel,
        contents,
        google_grounding: bool = False,
    ):
        if google_grounding:
            google_search = grounding.GoogleSearchRetrieval()
            grounding_tool = Tool.from_google_search_retrieval(google_search)
            raw_response = self.llm_model.generate_content(
                self.loaded_data, stream=True, tools=[grounding_tool]
            )
        else:
            raw_response = self.llm_model.generate_content(
                self.loaded_data, stream=True
            )
        return raw_response

    def process_generation_chunk(self, raw_responses):
        for raw_response in raw_responses:
            try:
                if len(raw_response.candidates) != 0:
                    yield raw_response.text, raw_response.candidates[0]
                else:
                    yield raw_response.text
            except (AttributeError, IndexError) as e:
                yield f"Error processing response: {e}, Raw response: {raw_response}"

    def load_files(self):
        if len(self.files) == 0:
            return []
        data = create_my_data_part(self.files)
        self.loaded_data = self.loaded_data + data

    def load_yt_link(self, yt_link: str):
        data = create_youtube_part(uri=yt_link)
        self.loaded_data = self.loaded_data + data
>>>>>>> 59d53e69ce24a2b81818fd40cf7b4181c0dfb01c
