import asyncio
from typing import List, Optional, Dict
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self, model : str, temperature : float , prompt : str, input_variables : List[str], output_type : Optional[BaseOutputParser] = StrOutputParser()):
        if temperature < 0.0 or temperature > 1.0:
            raise ValueError("temperature은 0.0과 1.0 사이의 값이여야합니다.")

        self.model_name = model # ex) gpt-turbo-3.5
        self.model = ChatOpenAI(model=model, temperature=temperature)
        self.prompt = PromptTemplate(
            template=prompt, input_variables=input_variables
        )
        self.input_variables = input_variables
        self.temperature = temperature
        self.output_type = output_type

        self.llm : Runnable = self.prompt | self.model | self.output_type

    async def invoke(self, inputs: Dict[str, str]):
        missing = [k for k in self.input_variables if k not in inputs]
        if missing:
            raise ValueError(f"누락된 입력 변수: {missing}")
        response = await self.llm.ainvoke(inputs)
        print(response)
        return response


# async def main(question : str):
#     model = "gpt-4o"
#     temperature = 0
#     prompt = "너는 {character}야. {question}"
#     input_variables = ["character", "question"]  # question도 포함해야 함
#
#     llm = LLM(model, temperature, prompt, input_variables)
#     response = await llm.invoke({
#         "character": "나루토",
#         "question": question
#     })
#     print(response)
#
# if __name__ == "__main__":
#     asyncio.run(main("나이가 몇살이니?"))
#     asyncio.run(main("이름이 무엇이니?"))
