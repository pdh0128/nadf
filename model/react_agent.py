from typing import Dict, Optional, List
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import StructuredTool, BaseTool
from langchain import hub  # Langchain hub에서 react 템플릿을 불러오기 위한 임포트
from model.llm import LLM

class ReactAgent(LLM):
    def __init__(self, model: str, temperature: float, prompt : str, input_variables: List[str], output_type: Optional[BaseOutputParser] = StrOutputParser(), tools: List[BaseTool] = list()):
        # 도구와 기타 파라미터 초기화
        self.tools = tools
        super().__init__(model, temperature, prompt, input_variables, output_type)  # prompt는 None으로, 나중에 hub에서 가져올 예정
        # Langchain hub에서 react agent 템플릿을 불러옵니다
        react_prompt = hub.pull("hwchase17/react")  # Langchain hub에서 react 템플릿을 불러옵니다
        self.model = self.model.bind(stop=["\nObservation:", "\nAction Input:"])  # 모델에서 특정 지점에서 멈추도록 설정
        self.agent = create_react_agent(self.model, self.tools, react_prompt)  # react agent 생성
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            return_intermediate_steps=True,
            max_iterations=4,
            early_stopping_method="force",
        )

    # 오버라이드
    async def invoke(self, inputs: Dict[str, str]):
        # 필요한 입력 변수가 누락되었는지 확인하고, 누락된 경우 에러 발생
        missing = [k for k in self.input_variables if k not in inputs]
        if missing:
            raise ValueError(f"누락된 입력 변수: {missing}")

        # prompt 준비
        prompt_tmpl = (self.prompt if isinstance(self.prompt, PromptTemplate)
                       else PromptTemplate.from_template(self.prompt))

        required = set(prompt_tmpl.input_variables)
        missing = [k for k in required if k not in inputs]
        if missing:
            raise ValueError(f"누락된 입력 변수: {missing}")

        # 입력값을 사용해 prompt를 포맷팅
        question = prompt_tmpl.format(**{k: inputs[k] for k in required})
        print(question)  # 포맷된 질문 출력 (선택적)

        # agent 실행 후 응답을 받음
        response = await self.executor.ainvoke({"input": question})
        print(response['output'])  # 응답 출력 (선택적)
        return response['output']
