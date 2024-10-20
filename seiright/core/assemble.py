import logging

from ..utils.utils import timer
from ._types import LLMProvider, LLMResponse
from .llms import get_llm
from .web_crawler import extract_text_from_url, reformat_extracted_text

logger = logging.getLogger(__name__)


class ComplianceChecker:

    def __init__(self, llm_provider: LLMProvider, model: str):
        self.llm_provider = llm_provider
        self.model = model

        self.llm = get_llm(provider=self.llm_provider, model=self.model)

    def webpage(self, url: str) -> str:
        return reformat_extracted_text(*extract_text_from_url(url=url))

    def create_user_prompt(self, text: str) -> str:
        return f"""You are given the following text from the webpage of a website.
        You need to assess whether the given website is compliant or not. The website text is within the triple backticks: 

        ```
        {text}
        ```
        """

    @timer
    def chat(self, url: str) -> LLMResponse:
        webcontent = self.webpage(url=url)
        logging.debug(f"crawled web content: {webcontent}")
        user_prompt = self.create_user_prompt(text=webcontent)
        logging.debug(f"{user_prompt=}")
        llm_response = self.llm.chat(user_prompt=user_prompt)
        return llm_response


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    checker = ComplianceChecker(
        llm_provider=LLMProvider.OPENAI, model="gpt-4o-2024-08-06"
    )
    response = checker.chat(url="https://mercury.com")
    print(response)
