from langchain_core.prompts import PromptTemplate

explain_prompt = PromptTemplate(
    input_variables=["resume_data", "match_data"],
    template="""
You are an HR AI assistant.

Based on the data below, give a simple explanation.

Resume Data:
{resume_data}

Match Data:
{match_data}

Rules:
- DO NOT invent new skills
- ONLY use given data
- Keep it simple
- Return in plain text
"""
)