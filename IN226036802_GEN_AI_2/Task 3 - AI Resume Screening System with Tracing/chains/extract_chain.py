import os
from langchain_groq import ChatGroq
from prompts.extract_prompt import extract_prompt

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

extract_chain = extract_prompt | llm