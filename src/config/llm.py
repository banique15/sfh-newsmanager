"""LLM client wrapper supporting multiple providers."""

from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from src.config.settings import settings


class LLMClient:
    """LLM client wrapper for multiple providers."""

    def __init__(self) -> None:
        """Initialize LLM client based on settings."""
        self.provider = settings.default_llm.lower()
        self.model_name = settings.default_model
        self._client: Any = None

    def get_llm(self) -> Any:
        """Get the configured LLM instance."""
        if self._client is not None:
            return self._client

        if self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY not configured")
            self._client = ChatOpenAI(
                model=self.model_name,
                api_key=settings.openai_api_key,
                temperature=0.7,
            )

        elif self.provider == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY not configured")
            self._client = ChatAnthropic(
                model=self.model_name,
                api_key=settings.anthropic_api_key,
                temperature=0.7,
            )

        elif self.provider == "google":
            if not settings.google_api_key:
                raise ValueError("GOOGLE_API_KEY not configured")
            self._client = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=settings.google_api_key,
                temperature=0.7,
            )

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

        return self._client


# Global LLM client
llm_client = LLMClient()


def get_llm() -> Any:
    """Get the global LLM instance."""
    return llm_client.get_llm()
