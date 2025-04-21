from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

API_KEY = os.environ.get("API_KEY", default="")


class VertexAI:
    def __init__(self, vertexAI: bool = False):
        if vertexAI:
            self.client = genai.Client(
                vertexai=True,
                project="",
                location="",
            )
        else:
            self.client = genai.Client(api_key=API_KEY)

    def generate_streaming(self, model, content):
        chunks = self.client.models.generate_content_stream(
            model=model, contents=content
        )
        return chunks

    def get_gemini_models(self):
        gemini_models = {}
        for model in self.client.models.list():
            if "gemini" in model.name:
                gemini_models[model.display_name] = model.name
        return gemini_models
