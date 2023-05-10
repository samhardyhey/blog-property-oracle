import os

from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

load_dotenv()

embedding_function = OpenAIEmbeddings(openai_api_key=os.environ["OPEN_API_KEY"])
llm = OpenAI(openai_api_key=os.environ["OPEN_API_KEY"])
