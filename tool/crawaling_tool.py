import re
from urllib.parse import unquote, urlparse
from exception.not_namuwiki_exception import NotNamuwikiException
from util.httpx_client_util import HttpxClient
from bs4 import BeautifulSoup, Comment

async def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # 1) style/script 태그 제거
    for t in soup(["style", "script"]):
        t.decompose()

    # 2) HTML 주석 제거
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()

    # 3) window.INITIAL_STATE 제거 (본문에 들어있는 경우)
    for el in soup.find_all(string=re.compile(r"window\.INITIAL_STATE")):
        el.extract()

    # 4) a 태그만 보존, 나머지 태그는 unwrap (텍스트만 남김)
    for tag in soup.find_all(True):
        if tag.name == "a":
            href = tag.get("href")
            tag.attrs = {}
            if href:
                tag["href"] = href
        else:
            tag.unwrap()


    # 5) 텍스트 정리 (여러 공백과 줄바꿈 제거)
    cleaned_html = str(soup)
    cleaned_html = re.sub(r'\s+', ' ', cleaned_html)  # 여러 공백을 하나의 공백으로
    cleaned_html = cleaned_html.strip()  # 양옆 공백 제거

    return str(soup)


async def extract_name(soup, url):
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    slug = unquote(urlparse(url).path.rsplit("/",1)[-1])
    return slug.replace("_"," ").strip()


async def crawling_namuwiki(url: str) -> BeautifulSoup:

    if "namu.wiki" not in url:
        raise NotNamuwikiException()

    http_client = HttpxClient()
    soup = await http_client.get(url)  # soup은 BeautifulSoup 객체라고 가정

    # res = await clean_html(soup.prettify())
    return soup

if __name__ == "__main__":
    url = "https://namu.wiki/w/%EC%9A%B0%EC%A6%88%EB%A7%88%ED%82%A4%20%EB%82%98%EB%A3%A8%ED%86%A0#s-2.1"
    url2 = "https://namu.wiki/w/%EA%B3%A0%ED%86%A0%20%ED%9E%88%ED%86%A0%EB%A6%AC/%EC%9D%B8%EB%AC%BC%20%EA%B4%80%EA%B3%84"
    print("end")
