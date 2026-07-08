from tools.llm import load_llm
from prompts.topic_generator import TOPIC_GENERATOR_PROMPT
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import TOPIC_GENERATOR_MODEL

model=load_llm(model_name=TOPIC_GENERATOR_MODEL)
parser=StrOutputParser()

prompt=PromptTemplate(template=TOPIC_GENERATOR_PROMPT,
                      input_variables=[]
                      )

chain=prompt | model | parser

def topic_generator_agent():
    return chain.invoke({})

