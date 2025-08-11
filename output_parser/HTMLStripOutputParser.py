from bs4 import BeautifulSoup
from langchain_core.output_parsers import BaseOutputParser

class HTMLStripOutputParser(BaseOutputParser[str]):
    def parse(self, text: str) -> str:
        return text.strip("`html")

    @property
    def _type(self) -> str:
        return "html_strip_output_parser"
