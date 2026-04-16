from langchain_core.prompts import PromptTemplate

match_prompt = PromptTemplate(
    input_variables=["resume_data", "job_description"],
    template="""
You are a resume matching system.

Input:
- resume_data (JSON)
- job_description (JSON)

IMPORTANT:
Return ONLY valid JSON.
Do NOT include:
- explanations
- markdown
- python code
- backticks
- text outside JSON

Task:
Return ONLY JSON in this format:

{{
  "matched_skills": [],
  "missing_skills": [],
  "score": 0
}}

IMPORTANT:
Return ONLY JSON. No python code. No explanation.
"""
)