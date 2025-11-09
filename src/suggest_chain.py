from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class TestIdea(BaseModel):
    title: str
    hypothesis: str
    rationale: str
    metrics: List[str]
    sample_size_hint: Optional[str] = None
    risks: List[str]
    instrumentation: List[str]

class Suggestions(BaseModel):
    overall_theme: str
    ideas: List[TestIdea]

HEURISTICS = """
Heuristics:
- If Win but lift < 5%, recommend cheap iteration: copy tweaks, placement, contrast.
- If Lose, recommend rollback, alternative hypothesis (intent cue, incentive framing), or channel segmentation.
- If Inconclusive, recommend power extension (longer run, larger sample), higher-signal proxy, or stronger contrast.
- Always include one instrumentation improvement (event quality, guardrails, attribution).
"""

STRICT_RULES = (
    "Return ONLY valid JSON that conforms exactly to the provided schema. "
    "No markdown, no code fences, no prose. "
    "All numbers must be plain JSON numbers (no NaN, Infinity, or strings). "
    "Do not add extra fields."
)

def build_suggestions_chain(model_name: str = "llama3"):
    llm = OllamaLLM(model=model_name, temperature=0.3)
    parser = PydanticOutputParser(pydantic_object=Suggestions)
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You propose practical next experiments grounded in the provided outcome and heuristics. "
         "Prefer low-effort, high-signal ideas. Output must follow the schema. " + STRICT_RULES),
        ("human",
         "Heuristics: {heuristics}\nOutcome: {verdict}\nKey learnings: {learnings}\nConstraints: {constraints}\n"
         "Latest experiment name: {name}\nHypothesis: {hypothesis}\n\n"
         "Propose exactly three ideas with a tight rationale and one instrumentation suggestion.\n"
         "{format_instructions}")
    ]).partial(format_instructions=parser.get_format_instructions())
    return prompt | llm | parser
