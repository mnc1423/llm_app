import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

DOTENV_PATH = os.environ.get(
    "DOTENV_PATH", os.path.join(os.path.dirname(__file__), ".env")
)


class _OllamaSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="OLLAMA_",
        env_file=DOTENV_PATH,
        extra="ignore",
        env_ignore_empty=True,
    )
    endpoint: Optional[str] = None
    model_path: Optional[str] = None


class _GoogleSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="GOOGLE_",
        env_file=DOTENV_PATH,
        extra="ignore",
        env_ignore_empty=True,
    )
    api_key: Optional[str] = None
    project: Optional[str] = None
    location: Optional[str] = None


class AppSettings(BaseSettings):
    ollama = _OllamaSettings = _OllamaSettings()
    google = _google = _GoogleSettings()


app_settings = AppSettings()
