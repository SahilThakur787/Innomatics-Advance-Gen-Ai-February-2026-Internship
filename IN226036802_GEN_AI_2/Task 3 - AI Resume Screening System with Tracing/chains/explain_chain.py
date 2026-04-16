import os
from langchain_groq import ChatGroq
from prompts.explain_prompt import explain_prompt

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

explain_chain = explain_prompt | llm