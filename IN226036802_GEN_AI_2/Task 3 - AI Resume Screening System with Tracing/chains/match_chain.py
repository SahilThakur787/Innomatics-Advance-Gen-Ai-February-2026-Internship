import os
from langchain_groq import ChatGroq

from langchain_groq import ChatGroq
from prompts.match_prompt import match_prompt
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")  # ensure explicit
)
match_chain = match_prompt | llm