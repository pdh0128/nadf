from model.react_agent import ReactAgent
from output_parser.HTMLStripOutputParser import HTMLStripOutputParser
from tool.crawaling_tool import crawling_namuwiki_tool

PARSING_PROMPT = """
다음은 나무위키에서 참고한 '{character}' 캐릭터 관련 문서이다.

[작성 목표]
- {character}의 세계관, 설정, 성격, 외형, 능력, 행적, 주요 사건과 관계, 캐릭터 분석을
  가능한 한 상세하고 풍부하게 작성한다.
- HTML 형식으로 작성하며, 제목(h1)과 소제목(h2~h4)을 사용해 체계적으로 구성한다.
- 절대 요약하지 말고, 정보량을 줄이지 않는다.
- 특히 '작중 행적'과 '주요 사건과 관계'는 반드시 길고 구체적으로 작성한다.

[세부 지시]
1. **작중 행적**:
   - 반드시 시간 순서로 서술.
   - 각 사건마다 시기·배경·인물·전투 과정·대사·감정 변화를 포함.
   - 중요 전투와 갈등은 상세히 묘사.
   - 단순 나열이 아니라 사건 간 인과관계와 캐릭터 성장 과정을 연결.

2. **주요 사건과 관계**:
   - 캐릭터와 밀접한 인물/집단별로 구분.
   - 관계 형성 계기, 갈등과 화해 과정, 상호 대사와 감정 변화를 서술.
   - 각 관계가 캐릭터 성장과 가치관에 끼친 영향을 분석.
   - 집단(가족, 팀, 조직 등)을 언급하는 경우, 반드시 구성원 목록과 각 구성원에 대한 개별 설명(h4)을 포함한다.

[제외해야 할 항목]
- 게임, 미디어믹스, 2차 창작, 팬덤 문화, 굿즈, 배우 정보 등
- 본문과 무관한 외부 자료, 링크, 광고성 내용

[출력 형식]
1. 문단은 <p>로 감싸고, 중요한 대사는 <blockquote> 사용.
2. 목록이 필요한 경우 <ul>과 <li> 사용.
3. HTML 태그는 반드시 올바르게 닫는다.

[크롤링 여부 체크]
1. 다음 항목들이 제공된 namuwiki_document에 포함되어 있는지 확인하세요:
- 행적
- 인간 관계
2. 모든 항목이 포함되어 있을 경우:
- 추가 크롤링을 건너뛰고, 제공된 namuwiki_document 데이터를 사용하여 캐릭터 소개글을 작성합니다.
3. 부족한 항목이 있을 경우:
- 부족한 항목에 대해서만 추가적으로 크롤링하여 정보를 보강합니다.
- 중요: 이미 크롤링된 데이터 안에서 더 깊은 정보를 추출하거나 재크롤링하지 않도록 합니다. 이미 크롤링한 데이터를 기반으로 해야 하며, 그 데이터를 더 파고들지 마세요.
4. 크롤링을 위해 필요한 URL:
- 부족한 항목에 대한 정보를 크롤링하기 위해 필요한 URL은 제공된 a 태그의 href 속성에 포함되어 있습니다.
- 이 URL을 사용하여 부족한 정보를 크롤링합니다.

[지시]
아래 참고 자료를 분석하여 위 규칙에 맞는 HTML 캐릭터 소개글을 생성하라.

[참고 자료]
다음 참고자료는 {character}의 나무위키 문서를 정리하여 제공한 문서이다.
{namuwiki_document}
"""

pdf_writer_agent = ReactAgent(
    "gpt-4o",
    0,
    prompt=PARSING_PROMPT,
    input_variables=["character", "namuwiki_document"],
    output_type=HTMLStripOutputParser(),
    tools=[crawling_namuwiki_tool],
)

async def write(content : str):
    response = await pdf_writer_agent.invoke({
        "character": name,
        "namuwiki_document": safe_doc,
    })