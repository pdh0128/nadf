import asyncio, os
from model.pdf import PDF
from util.crawaling_util import crawling_namuwiki
from util.html_parser_util import HtmlParser
from collections import deque

async def html_to_pdf(title: str, content: str, output_path: str, doc_title: str = "문서 제목"):
    pdf = PDF(doc_title=doc_title)
    pdf.add_page()

    pdf.chapter_title(title)
    pdf.chapter_body(content)
    pdf.output(output_path)

skip_titles = {"게임", "미디어 믹스", "둘러보기"}
base_url = "https://namu.wiki"

async def get_namuwiki_list(url):
    # 메인 페이지 HTML
    main_html = await crawling_namuwiki(url)
    main_parser = HtmlParser(main_html, url)
    # 이름 추출
    name = await main_parser.extract_name()
    print(name)
    small_topics = await main_parser.extract_small_topics()
    print(small_topics)
    namuwiki_list = []
    content_list = await main_parser.extract_content()
    print(content_list[0])

    content_list_dq = deque(content_list)
    for title, uri, level in small_topics:
        print(f"title : {title}")
        if title.strip() in skip_titles:
            continue

        if uri.startswith("/w") and level == 'h2':
            content_list_dq.popleft()
            full_url = base_url + uri
            html = await crawling_namuwiki(full_url)
            parser = HtmlParser(html, full_url)
            data = await extract_page_data(parser)
            data = [x for x in data if x[0].strip() not in skip_titles]
            namuwiki_list.extend(data)

        else:
            content = content_list_dq.popleft()
            if title == "어록":
                print(content)
            namuwiki_list.append((title, content, level))
    return name, namuwiki_list


async def namuwiki_to_pdf(url: str):
    name, namuwiki_list = await get_namuwiki_list(url)
    # PDF 생성
    doc_title = f"{name} 분석 보고서"
    output_path = f"./{doc_title}.pdf"

    pdf = PDF(doc_title=doc_title)
    output_path = await pdf.create_pdf_from_namuwiki_list(namuwiki_list, output_path)
    return output_path

async def extract_page_data(parser: HtmlParser) -> list[tuple[str, str, str]]:
    small_topics = await parser.extract_small_topics()

    # print(small_topics)
    content = await parser.extract_content()
    print(len(small_topics), len(content))
    if len(small_topics) != len(content):
        print(parser.url)
    return [(title, body, level) for (title, _, level), body in zip(small_topics, content)]

if __name__ == "__main__":
    url = "https://namu.wiki/w/%EB%82%98%EB%A3%A8%ED%86%A0"
    asyncio.run(namuwiki_to_pdf(url))
