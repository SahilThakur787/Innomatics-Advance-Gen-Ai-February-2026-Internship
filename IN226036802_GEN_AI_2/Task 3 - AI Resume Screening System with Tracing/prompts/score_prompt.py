from langchain_core.prompts import PromptTemplate

score_prompt = PromptTemplate(
    input_variables=["match_data"],
    template="""
You are an AI evaluator.

Assign a score between 0 to 100.

Rules:
- More matched skills = higher score
- Missing key skills = reduce score
- Return ONLY number

IMPORTANT:
Return ONLY valid JSON.
Do NOT include:
- explanations
- markdown
- python code
- backticks
- text outside JSON

Match Data:
{match_data}
"""
)