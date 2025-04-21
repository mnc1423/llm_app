from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

API_KEY = os.environ.get("GOOGLE_API_KEY", default="")
PROJECT = os.environ.get("project", default="")
LOCATION = os.environ.get("location", default="")


class GeminiClient:
    def __init__(self, vertexAI: bool = False):
        if vertexAI:
            self.client = genai.Client(
                vertexai=True,
                project="",
                location="",
            )
        else:
            self.client = genai.Client(api_key=API_KEY)
        self.content_loader = ContentLoader()
        self.contents = []  # contents

    def generate_streaming(self, model):
        chunks = self.client.models.generate_content_stream(
            model=model, contents=self.contents
        )
        return chunks

    def get_gemini_models(self):
        gemini_models = {}
        for model in self.client.models.list():
            if "gemini" in model.name:
                gemini_models[model.display_name] = model.name
        return gemini_models

    def create_content_list(self, history_list: list):
        # history_list.append(prompt)
        text_data = self.content_loader.load_text_data(history_list)
        self.contents = self.contents + text_data


class ContentLoader:
    def __init__(self):
        pass

    def load_text_data(self, content_list):
        text_data = [
            types.Content(
                role=con["role"], parts=[types.Part.from_text(text=con["content"])]
            )
            for con in content_list
        ]

        return text_data

    def load_file(self, file_data, mime_type):
        file_data = [
            types.Content(
                role="user",
                parts=[types.Part.from_bytes(data=file_data, mime_type=mime_type)],
            )
        ]
        return file_data
