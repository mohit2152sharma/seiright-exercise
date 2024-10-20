import textwrap
from typing import Optional, cast

import requests
from bs4 import BeautifulSoup, Tag


def extract_text_from_url(url: str) -> tuple[str, str | None]:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.find("title")
    if isinstance(title_tag, Tag):
        title = title_tag.get_text(strip=True) or None
    else:
        title = None

    text_elements = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li"])

    extracted_text = []
    for element in text_elements:
        text = element.get_text(strip=True)
        if text:
            if element.name.startswith("h"):
                extracted_text.append(f"\n{'#' * int(element.name[1:])} {text}\n")
            else:
                extracted_text.append(text)

    return cast(str, "\n".join(extracted_text)), title


def reformat_extracted_text(text: str, title: Optional[str] = None) -> str:
    result = ""
    if title:
        x = f"Title: {title}"
        result = f"{x:=^100}\n"

    wrapped_text = textwrap.fill(
        text, width=80, break_long_words=False, replace_whitespace=False
    )
    return result + wrapped_text
