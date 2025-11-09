from __future__ import annotations
from typing import List
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class MetricResult(BaseModel):
    metric: str
    baseline_value: float
    treatment_value: float
    lift: float
    p_value: float
    ci: List[float]  # [low, high]

class ExperimentSummary(BaseModel):
    title: str
    verdict: str
    summary: str
    key_metrics: List[MetricResult]
    drivers: List[str]
    caveats: List[str]
    recommended_actions: List[str]

STRICT_RULES = (
    "Return ONLY valid JSON that conforms exactly to the provided schema. "
    "No markdown, no code fences, no prose. "
    "All numbers must be plain JSON numbers (no NaN, Infinity, or strings). "
    "Do not add extra fields."
)

def build_summarize_chain(model_name: str = "llama3"):
    llm = OllamaLLM(model=model_name, temperature=0.2)
    parser = PydanticOutputParser(pydantic_object=ExperimentSummary)
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an experimentation analyst. Be precise, terse, and actionable. "
         "Use only the numbers supplied in stats_json. Do not invent numbers. "
         "If data is insufficient or variance is high, mark Inconclusive and list caveats. "
         + STRICT_RULES),
        ("human",
         "Experiment: {name}\nHypothesis: {hypothesis}\nPrimary metric: {primary_metric}\n"
         "Stats (json): {stats_json}\nSegments (optional json): {segments_json}\n\n"
         "Write a structured summary.\n{format_instructions}")
    ]).partial(format_instructions=parser.get_format_instructions())
    return prompt | llm | parser
