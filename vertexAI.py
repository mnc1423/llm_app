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



    