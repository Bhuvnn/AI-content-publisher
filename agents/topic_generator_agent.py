from tools.llm import load_llm
from prompts.topic_generator import TOPIC_GENERATOR_PROMPT
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import TOPIC_GENERATOR_MODEL
from database.crud import get_recent_topics

model=load_llm(model_name=TOPIC_GENERATOR_MODEL)
parser=StrOutputParser()

prompt=PromptTemplate(template=TOPIC_GENERATOR_PROMPT,
                      input_variables=["recent_topics"]
                      )

chain=prompt | model | parser

def topic_generator_agent():
    recent_topics_list = get_recent_topics(10)
    if recent_topics_list:
        recent_topics_str = "\n".join(f"- {topic}" for topic in recent_topics_list)
    else:
        recent_topics_str = "None yet."
    return chain.invoke({"recent_topics": recent_topics_str})

