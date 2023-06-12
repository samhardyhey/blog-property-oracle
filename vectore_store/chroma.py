from pathlib import Path

from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from llm import embedding_config
from utils import logger

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

vectordb_persist_dir = str(Path(__file__).parents[1] / "db")
vectordb = Chroma(
    embedding_function=embedding_config, persist_directory=vectordb_persist_dir
)


def ingest_transcript_df_chromadb(transcript_df, transcript_col):
    # TODO: add upsert, prevent redundant writes
    documents = DataFrameLoader(
        transcript_df, page_content_column=transcript_col
    ).load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=0
    )
    texts = text_splitter.split_documents(documents)
    logger.info(
        f"Supplied {len(transcript_df)} records, ingesting as {len(texts)} documents"
    )
    vectordb.add_documents(texts)
    vectordb.persist()
