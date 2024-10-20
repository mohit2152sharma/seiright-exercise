"""Abstraction over how llms consume prompts"""

from pathlib import Path
from typing import cast

from ._types import PromptRoles


def prompts_dir() -> Path:
    return Path(__file__).parent.joinpath("prompts")


def get_prompt(role: PromptRoles) -> str:
    file = prompts_dir().joinpath(f"{cast(str, role)}.txt")
    with open(file, "r") as f:
        return f.read()


class SeiPrompts:
    system_prompt: str = get_prompt("system")
