import os
from langchain_groq import ChatGroq

from langchain_groq import ChatGroq
from prompts.score_prompt import score_prompt
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")  # ensure explicit
)
score_chain = score_prompt | llm