import asyncio

import tiktoken
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.runnables import Runnable

from model.llm import LLM

class SummaryLLM(LLM):
    def __init__(self, model: str, temperature: float):
        # 부모 LLM 클래스의 초기화 호출
        prompt_template = """
     다음 텍스트를 간결하고 정보성 있게 요약하시오:
     나무위키에 대한 정보는 제거하세요.
    
    {input}
        """

        # SummaryLLM의 프롬프트 템플릿 설정
        super().__init__(model, temperature, prompt_template, input_variables=["input"])

        # 요약을 위한 LLMChain 정의 (PromptTemplate -> Model -> OutputParser)
        self.llm : Runnable = self.prompt | self.model | self.output_type

    async def summarize(self, text: str) -> str:
        # 텍스트를 청크로 나누는 함수
        def split_text_into_chunks(data: str, max_tokens: int = 30000) -> list:
            encoding = tiktoken.get_encoding("cl100k_base")
            tokenized_data = encoding.encode(data)

            chunks = []
            current_chunk = []
            current_tokens = 0

            for token in tokenized_data:
                if current_tokens + 1 <= max_tokens:
                    current_chunk.append(token)
                    current_tokens += 1
                else:
                    chunks.append(encoding.decode(current_chunk))
                    current_chunk = [token]
                    current_tokens = 1

            if current_chunk:
                chunks.append(encoding.decode(current_chunk))

            return chunks

        # 텍스트를 청크로 나누기
        chunks = split_text_into_chunks(text)

        # 각 청크에 대해 요약을 수행하고 결과를 합침
        summarized_chunks = []
        for chunk in chunks:
            try:
                # 비동기적으로 요약 (타임아웃 설정)
                summary = await asyncio.wait_for(self.llm.ainvoke(input=chunk), timeout=30)  # 30초 타임아웃
                print(summary)
                summarized_chunks.append(summary)
            except asyncio.TimeoutError:
                print(f"요약 시간이 초과되었습니다: {chunk}")
                summarized_chunks.append("요약 실패")

        # 요약된 모든 청크를 합쳐서 반환
        return " ".join(summarized_chunks)


if __name__ == "__main__":
    summary = SummaryLLM(model="gpt-4o", temperature=1.0)
    data = """이런 어린 시절에 관하여 나뭇잎 마을의 인물들,[4] 특히 미나토와 접점이 있던 대부분의 인물들에게 설붕이 생긴다. 제자이자 부하였고, 미나토가 특별히 그의 트라우마를 걱정해 측근으로 두고 보살폈던 카카시는 처음 7반 결성시 나루토의 자기소개를 듣고 '이녀석 상당히 재미있는 성장을 했군.'이라고 독백하는데, 이는 그동안 나루토가 어떻게 지내고 있는지 몰래 가 보거나 하는 관심조차 전혀 쏟지 않았다는 말이 된다. 나루토에게 있어서의 이루카 정도까지는 아니더라도 카카시에게 있어서도 미나토는 소중한 스승이었고, 미나토 반이 전멸한 지금 나루토는 그 인연의 마지막 끈이나 다름이 없었음에도 신경을 쓰지 않았다는 점에는 괴리감이 든다. 심지어 미나토는 카카시의 힐링에 도움되라고 카카시에게 나루토를 임신한 쿠시나의 호위까지 맡긴 적이 있었는데 말이다! 그외에도 미나토의 상급 닌자 시절 구름마을 에이-비 형제와 겨룰 때에도 함께 있었고 그외에도 이런저런 임무를 함께 해 왔을 것으로 보이는 아키미치 쵸자[5]는 1화에서 보면 아예 나루토를 없애버리자는 선동에 동조하고 있는 장면이 나온다.[6]

게다가 지라이야는 쿠시나로부터 직접 나루토의 이름이 자신의 소설에서 나온 등장인물에 따온 것에 대부가 되는 것이냐면서 감동하는 모습을 보이기도 했는데, 정작 나루토를 처음 만났을 때 미나토의 아들이라는 것을 알아보는 듯한 장면은 없었다. 즉, 제자가 죽은 것을 알았지만 정작 제자의 아들은 신경쓰지 않았다는 모순이 발생하게 된다. 심지어 2년 동안 함께 다녔는데도 나루토는 지라이야로부터 자신의 아버지가 4대라는 정보를 듣지 못하기도 했고...[7]

또 이후에 미나토 본인이 선인모드를 쓸 수 있다는 것과, 가마분타를 미나토가 소환했다는 것 또한 밝혀졌는데, 가마분타는 물론이고 묘목산의 두꺼비들조차 미나토에 대한 언급은 조금도 없던 것 또한 의문이다. 2대 선인인 후카사쿠는 과거 나루토에게 선술을 가르쳤을 때 아무나 이런 선술을 배우는 것이 가능한것이 아니라고 말하면서 오직 지라이야와 나루토만이 배울 수 있다고 말을 하였고, 이후에 나루토가 성공적으로 선술을 배웠을 때도 오직 지라이야와 비교만 하였지 미나토에 대한 언급조차 없었으니.

결정적으로 나루토의 정체를 나뭇잎 마을에서 몰랐다는 것 또한 의문이 가는데 미나토의 금발과 벽안이 흔한 것도 아니고 친근하게 지내면서 서로를 다 알고 지내는 마을에서, 미나토의 사망과 당시의 쿠시나가 만삭이었음 등등을 카카시와 쵸자를 포함한 대부분의 닌자들이 몰랐을 리도 없다. 심지어 우즈마키 일족은 작중 시점에서는 거의 멸족 상태여서 흔한 성도 아니었을 거고, 초대 호카게의 아내와 4대 호카게의 아내가 우즈마키 일족인데,[8] 나루토가 이들과 모종의 연관이 있을 수 있다는 것조차 다른 이들이 짐작하지 못했다는 것 또한 상식적으로 납득이 가지 않는다.

결국 이런 오류를 방지하려면 적어도 미나토와 동시기에 활발히 활동하던, 작중 초반에 주민들은 아니더라도 사정을 아는 닌자 몇명 정도는 나루토에게 남몰래라도 따뜻한 관심을 보내고 격려해 주거나 돕는 묘사가 들어가야 했다. 하지만 그러면 나루토의 참담한 현실을 보여주는데 방해가 되고 그저 부모도 없는 인주력인 줄 알았던 나루토가 사실은 마을을 구한 영웅인 4대의 아들로 밝혀질 때의 임팩트와 영혼이 된 상태의 미나토와 쿠시나를 만났을 때의 감동이 상대적으로 약해질 수 있었기에 이런 모습은 전혀 나오지가 않았다. 게다가 이후에 미나토가 나루토의 아버지인 것이 밝혀지면서 선인모드를 비롯한 설정이 붙었지만, 이 역시 이전에 있던 설정과 맞지 않으면서 설정구멍이 생기고 말았다. 즉 후반부의 반전과 감동을 부각시키기 위한 어쩔 수 없던 연출, 혹은 생각하지도 않았던 장면이였던[9] 셈.

사실 미나토의 존재를 고려하지 않더라도 마을 사람들이 나루토를 험하게 대하는 것 자체도 좀체 납득하기 힘든 부분이 있는데, 초반부의 몇몇 어른들이나 에비스같은 캐릭터들은 나루토를 괴물 구미호라고 혐오하고 인격적으로 그를 깎아내리고 욕하는 모습을 보인바가 있다. 하지만 나루토는 어디까지나 구미호가 봉인되어 있을뿐인 아이일 뿐 본인이 사악한이거나 인격적으로 못난 존재는 아니었다(말 그대로 개구쟁"""
    print(asyncio.run(summary.summarize(data)))

