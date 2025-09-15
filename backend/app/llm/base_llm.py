from abc import ABC, abstractmethod
from typing import Union, List, Literal
from langchain.schema import AIMessage


class BaseLLM(ABC):
    @abstractmethod
    def get_llm(self):
        pass

    @abstractmethod
    def test_llm(self) -> tuple[Literal[False], str] | bool:
        pass

    @abstractmethod
    def chat(self, query: str, system_prompt: str = "", context: str = "") -> AIMessage:
        """
        Interacts with a chat-based model.

        Args:
            messages (List[BaseMessage]): A list of message objects (e.g., HumanMessage, AIMessage).

        Returns:
            str: The content of the AI's response message.
        """
        pass

    @abstractmethod
    def get_embedding(self, text: str) -> list[float]:
        """
        Interacts with an embedding model.

        Args:
            text: Text for generating embedding

        Returns:
            List[float]: Embedding vector of the text.
        """
        pass
