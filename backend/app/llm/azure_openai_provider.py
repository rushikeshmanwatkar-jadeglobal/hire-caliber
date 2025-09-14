from openai import AzureOpenAI
from typing import Literal

from app.core.config import settings


class AzureOpenAIProvider:

    def __init__(
        self,
        type: Literal["chat", "embedding"],
        **kwargs,
    ) -> None:
        try:
            self.type = type
            if type != "chat" and type != "embedding":
                raise ValueError("Invalid type for llm provider")
            if type == "chat":
                self.deployment_name = settings.CHAT_MODEL_NAME
            else:
                self.deployment_name = settings.EMBEDDING_MODEL_NAME
            self.api_key = settings.AZURE_OPENAI_API_KEY
            self.azure_endpoint = settings.AZURE_OPENAI_ENDPOINT
            self.openai_api_version = settings.OPENAI_API_VERSION
            self.client = AzureOpenAI(
                azure_endpoint=self.azure_endpoint,
                api_key=self.api_key,
                api_version=self.openai_api_version,
            )
        except Exception as e:
            print(f"Error initializing AzureOpenAIProvider: {e}")
            raise e

    def embeddings(self, input, **kwargs):  # type: ignore
        return self.client.embeddings.create(
            input=input, model=self.deployment_name, **kwargs
        )

    def chat(self, messages, **kwargs):
        return self.client.chat.completions.create(
            messages=messages, model=self.deployment_name, **kwargs
        )
