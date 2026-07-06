from tools.llm import load_llm
from prompts.writer import WRITER_PROMPT
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from graph.state import WriterResult

model=load_llm()
parser=JsonOutputParser(pydantic_object=WriterResult)
prompt=PromptTemplate(template=WRITER_PROMPT,
                      input_variables=["topic", "research", "previous_poem", "critic_feedback"],
                      partial_variables={
                        "format_instructions": parser.get_format_instructions()
                }
                    )

chain=prompt | model | parser

def writer_agent(topic, research, previous_poem="", critic_feedback=""):
    return chain.invoke({
        "topic": topic,
        "research": research,
        "previous_poem": previous_poem,
        "critic_feedback": critic_feedback
    })

