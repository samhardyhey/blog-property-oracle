from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from llm import embedding_function

vectordb_persist_dir = "db"
vectordb = Chroma(
    embedding_function=embedding_function, persist_directory=vectordb_persist_dir
)


def ingest_transcript_df_chromadb(transcript_df, transcript_col):
    # TODO: add upsert, prevent redundant writes
    documents = DataFrameLoader(
        transcript_df, page_content_column=transcript_col
    ).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    vectordb.add_documents(texts)
    vectordb.persist()
