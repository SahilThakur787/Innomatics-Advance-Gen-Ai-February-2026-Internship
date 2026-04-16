from langchain_core.prompts import PromptTemplate

extract_prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
You are a resume parser.

Extract ONLY the following from the resume:

Return ONLY valid JSON:
{{
  "skills": [],
  "experience": "",
  "tools": []
}}

Resume:
{resume}

IMPORTANT:
- Return ONLY JSON
- No explanation
- No markdown
"""
)