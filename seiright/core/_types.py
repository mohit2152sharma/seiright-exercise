from enum import StrEnum
from typing import Literal

from pydantic import BaseModel

# type LLMProvider = Literal["openai", "anthropic", "google", "azure", "other"]


class LLMProvider(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"


class SchemaProperty(BaseModel):
    type: Literal["string", "number", "array", "object", "boolean", "float"]
    description: str


class LLMResponseSchema(BaseModel):
    type: str
    properties: dict[str, SchemaProperty]


class LLMResponse(BaseModel):
    model: str
    llm_provider: LLMProvider
    is_compliant: bool
    reasoning: str
    input_msg: str
    confidence_score: float


class PromptContent(BaseModel):
    type: str
    text: str


type PromptRoles = Literal["user", "assistant", "system"]


class PromptMessages(BaseModel):
    role: PromptRoles
    content: list[PromptContent]


class Prompt(BaseModel):
    messages: list[PromptMessages]
