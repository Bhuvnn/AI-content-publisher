from typing import TypedDict
from pydantic import BaseModel

class ResearchResult(BaseModel):
    core_idea: str
    themes: list[str]
    emotions: list[str]
    keywords: list[str]
    imagery: list[str]
    perspective: str
    writing_style: str
    guidance: str

class CriticResult(BaseModel):
    score: float
    strengths: list[str]
    weaknesses: list[str]
    feedback: str

class WriterResult(BaseModel):
    title: str
    content: str

class poemState(TypedDict):
    topic: str
    iteration: int
    research: ResearchResult
    content: WriterResult
    formatted_content: str
    critic: CriticResult