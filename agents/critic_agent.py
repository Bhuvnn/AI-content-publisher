from tools.llm import load_llm
from prompts.critic import CRITIC_PROMPT
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from graph.state import CriticResult

model=load_llm()
parser=JsonOutputParser(pydantic_object=CriticResult)
prompt=PromptTemplate(template=CRITIC_PROMPT,
                      input_variables=["topic", "research", "content"],
                      partial_variables={
                        "format_instructions": parser.get_format_instructions()
                }
                    )

chain=prompt | model | parser

def critic_agent(topic, research, content):
    return chain.invoke({"topic":topic, "research":research, "content": content})

