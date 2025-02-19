import os

import pinecone
from dotenv import load_dotenv

from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from property_oracle.llm import embedding_config

load_dotenv()

PINECONE_KEY = os.environ["PINECONE_KEY"]
PINECONE_ENV = os.environ["PINECONE_ENV"]

# initialize pinecone
pinecone.init(api_key=PINECONE_KEY, environment=PINECONE_ENV)
index_name = "langchain-demo"

# optionally create
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536)

pinecone_index = pinecone.Index(index_name)
pinecone_vector_db = Pinecone.from_existing_index(
    index_name, embedding=embedding_config, text_key="text"
)


def ingest_transcript_df_pinecone(transcript_df, transcript_col):
    documents = DataFrameLoader(
        transcript_df.head(20), page_content_column=transcript_col
    ).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    pinecone_vector_db.add_documents(texts)
