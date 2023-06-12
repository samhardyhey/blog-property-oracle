from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from property_oracle.config import DATA_DIR
from property_oracle.llm import embedding_config
from property_oracle.utils import logger

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 0

vectordb_persist_dir = DATA_DIR.parents[0] / "db"
if vectordb_persist_dir.exists() == False:
    vectordb_persist_dir.mkdir(parents=True, exist_ok=True)
vectordb = Chroma(
    embedding_function=embedding_config, persist_directory=str(vectordb_persist_dir)
)


def ingest_transcript_df_chromadb(transcript_df, transcript_col):
    # TODO: add upsert, prevent redundant writes
    documents = DataFrameLoader(
        transcript_df, page_content_column=transcript_col
    ).load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    texts = text_splitter.split_documents(documents)
    logger.info(
        f"Supplied {len(transcript_df)} records, ingesting as {len(texts)} documents"
    )
    vectordb.add_documents(texts)
    vectordb.persist()
