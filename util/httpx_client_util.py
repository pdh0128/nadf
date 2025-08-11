from bs4 import BeautifulSoup
from httpx import AsyncClient


HEADERS = {
    "User-Agent": "Mozilla/5.0 ... Safari/537.36"
}

class HttpxClient():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HttpxClient, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.client = AsyncClient(headers=HEADERS)

    async def get(self, url : str, timeout : int = 30):
       res  = await self.client.get(url, timeout=timeout)
       res.raise_for_status()
       soup = BeautifulSoup(res.content, "html.parser")
       return soup

    def __del__(self):
        self.client.aclose()
