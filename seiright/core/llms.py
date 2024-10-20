"""An abstraction over different llm providers"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Any

import yaml
from anthropic import Anthropic
from openai import OpenAI

from ..utils.utils import get_env_var
from ._types import (
    LLMProvider,
    LLMResponse,
    LLMResponseSchema,
    Prompt,
    PromptContent,
    PromptMessages,
    SchemaProperty,
)
from .prompts import SeiPrompts, prompts_dir

logger = logging.getLogger(__name__)


class LLM(ABC):

    def __init__(self, model: str, llm_provider: LLMProvider):
        self.model = model
        self.llm_provider = llm_provider

    @property
    def api_key(self) -> str:
        provider = str(self.llm_provider.value.upper())
        return get_env_var(f"{provider}_API_KEY", raise_error=True)

    @abstractmethod
    def chat(self, user_prompt: str) -> LLMResponse:
        pass

    @abstractmethod
    def create_prompt(self, msg: str) -> Prompt:
        pass

    @abstractmethod
    def response_format(self) -> dict[str, str]:
        pass

    @property
    def properties(self) -> LLMResponseSchema:
        dir = prompts_dir()
        properties_file = dir.joinpath("properties.yaml")
        with open(properties_file, "r") as f:
            props = yaml.safe_load(f.read())
        _r = {}
        for prop in props:
            _r[prop["name"]] = SchemaProperty(
                type=prop["type"], description=prop["description"]
            )
        return LLMResponseSchema(type="object", properties=_r)


class OpenAILLM(LLM):
    def __init__(self, model: str):
        super().__init__(model=model, llm_provider=LLMProvider.OPENAI)
        self.client = OpenAI(api_key=self.api_key)

    def create_prompt(self, user_prompt: str) -> Prompt:
        system_prompt = SeiPrompts.system_prompt
        system_content = PromptContent(type="text", text=system_prompt)
        user_content = PromptContent(type="text", text=user_prompt)
        return Prompt(
            messages=[
                PromptMessages(role="system", content=[system_content]),
                PromptMessages(role="user", content=[user_content]),
            ]
        )

    def response_format(self) -> dict[str, Any]:
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "compliance_response",
                "description": "Returns the compliance response for the given input in a structured json format",
                "strict": True,
                "schema": {
                    **self.properties.model_dump(),
                    "required": ["is_compliant", "reasoning", "confidence_score"],
                    "additionalProperties": False,
                },
            },
        }

    def chat(self, user_prompt: str) -> LLMResponse:
        llm_prompt = self.create_prompt(user_prompt=user_prompt)
        messages = [x.model_dump() for x in llm_prompt.messages]
        logger.debug(messages)
        rf = self.response_format()
        logger.debug(f"response format: {rf}")
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, response_format=rf
        )

        content = response.choices[0].message.content
        if content:
            content = json.loads(content)
            return LLMResponse(
                model=self.model,
                llm_provider=self.llm_provider,
                is_compliant=content["is_compliant"],
                reasoning=content["reasoning"],
                confidence_score=content["confidence_score"],
                input_msg=user_prompt,
            )
        else:
            raise RuntimeError(
                f"Unable to generate response for {user_prompt}. model={self.model}, llm_provider={self.llm_provider}"
            )


class AnthropicLLM(LLM):
    def __init__(self, model: str):
        super().__init__(model=model, llm_provider=LLMProvider.ANTHROPIC)
        self.client = Anthropic(api_key=self.api_key)

    def create_prompt(self, user_prompt: str) -> Prompt:
        user_content = PromptContent(type="text", text=user_prompt)
        return Prompt(messages=[PromptMessages(role="user", content=[user_content])])

    def response_format(self) -> dict[str, Any]:
        return {
            "name": "compliance_response",
            "description": "Returns the compliance response for the given input in a structured json format",
            "input_schema": self.properties.model_dump(),
        }

    def chat(self, user_prompt: str) -> LLMResponse:
        llm_prompt = self.create_prompt(user_prompt=user_prompt)
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[x.model_dump() for x in llm_prompt.messages],
            tools=[self.response_format()],
            tool_choice={"type": "tool", "name": "compliance_response"},
        )

        c = [x.input for x in response.content if x.type == "tool_use"]
        if c:
            return LLMResponse(
                model=self.model,
                llm_provider=self.llm_provider,
                is_compliant=c["is_compliant"],
                reasoning=c["reasoning"],
                confidence_score=c["confidence_score"],
                input_msg=user_prompt,
            )
        else:
            raise RuntimeError(
                f"Unable to generate response for {user_prompt}. model={self.model}, llm_provider={self.llm_provider}"
            )


class AzureLLM(LLM):
    def __init__(self, model: str):
        super().__init__(model=model, llm_provider=LLMProvider.AZURE)
        raise NotImplementedError


def get_llm(provider: LLMProvider, model: str) -> OpenAILLM | AnthropicLLM:
    llm_classes = {
        LLMProvider.OPENAI: OpenAILLM,
        LLMProvider.ANTHROPIC: AnthropicLLM,
        LLMProvider.AZURE: AzureLLM,
    }
    return llm_classes[provider](model)
