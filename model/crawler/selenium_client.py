import asyncio

from bs4 import BeautifulSoup

from model.crawler.crawler_client import CrawlerClient
import undetected_chromedriver as uc

class SeleniumClient(CrawlerClient):
    def __init__(self):
        self.options = uc.ChromeOptions()
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--headless=new')
        self.driver = uc.Chrome(options=self.options)

    # override
    async def get(self, url : str):
        await asyncio.to_thread(self.driver.get, url)

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        print(soup)
        return soup


if __name__ == '__main__':
    client = SeleniumClient()
    print(asyncio.run(client.get("https://namu.wiki/w/%EB%82%98%EB%A3%A8%ED%86%A0")))

