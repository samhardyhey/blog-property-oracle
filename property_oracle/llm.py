import os

from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

load_dotenv()

embedding_config = OpenAIEmbeddings(openai_api_key=os.environ["OPEN_API_KEY"])
llm = OpenAI(openai_api_key=os.environ["OPEN_API_KEY"])

example_questions = [
    "What are the basic steps I need to complete before attempting to purchase property in Australia?",
    "If I'm a first home buyer, what are some things I need to be mindful of when buying?",
    "What are the steps involved in getting finance pre-approval?",
    "Should I use mortgage broker? And if so, why?",
    "Does it matter if I can't put together a 20% deposit? What are my options?",
    "What is the general effect of a recession on house prices? Is this a good time to buy?",
    "What are some important differences between on and off-market properties?",
    "Can you write me a to-do list for first home buyer?",
]
