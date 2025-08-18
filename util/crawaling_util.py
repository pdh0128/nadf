from exception.not_namuwiki_exception import NotNamuwikiException
from model.crawler.httpx_client import HttpxClient
from bs4 import BeautifulSoup

from model.crawler.selenium_client import SeleniumClient


async def crawling_namuwiki(url: str) -> BeautifulSoup:

    if "namu.wiki" not in url:
        raise NotNamuwikiException()

    http_client = SeleniumClient()
    soup = await http_client.get(url)  # soup은 BeautifulSoup 객체라고 가정

    # res = await clean_html(soup.prettify())
    return soup

if __name__ == "__main__":
    url = "https://namu.wiki/w/%EC%9A%B0%EC%A6%88%EB%A7%88%ED%82%A4%20%EB%82%98%EB%A3%A8%ED%86%A0#s-2.1"
    url2 = "https://namu.wiki/w/%EA%B3%A0%ED%86%A0%20%ED%9E%88%ED%86%A0%EB%A6%AC/%EC%9D%B8%EB%AC%BC%20%EA%B4%80%EA%B3%84"
    print("end")
