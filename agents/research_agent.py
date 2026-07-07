from tools.llm import load_llm
from prompts.research import RESEARCH_PROMPT
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from graph.state import ResearchResult
from app.config import RESEARCH_MODEL

model=load_llm(model_name=RESEARCH_MODEL)
parser=JsonOutputParser(pydantic_object=ResearchResult)
prompt=PromptTemplate(template=RESEARCH_PROMPT,
                      input_variables=["topic"],
                      partial_variables={
                    "format_instructions": parser.get_format_instructions()
                    }
                    )

chain=prompt | model | parser

def research_agent(topic):
    return chain.invoke({"topic":topic})

