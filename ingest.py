import os

import pandas as pd
from langchain.chains import VectorDBQA
from langchain.document_loaders import DataFrameLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from transcribe import transcript_dir

transcript_col = "text"
embedding_function = OpenAIEmbeddings(openai_api_key=os.environ["OPEN_API_KEY"])
llm = OpenAI(openai_api_key=os.environ["OPEN_API_KEY"])
vectordb_persist_dir = "db"
vectordb = Chroma(
    embedding_function=embedding_function, persist_directory=vectordb_persist_dir
)
merge_threshold = 2


def merge_adjacent_utterances(df):
    # Merge records
    merged_records = []
    for _, row in df.iterrows():
        if row["merge"]:
            # Merge text with the next recordb
            row["text"] += df.loc[_, "text"]
            row["end"] = df.loc[_, "end"]
            # Remove the next record from the dataframe
            df.drop(_, inplace=True)
        merged_records.append(row)
    return (
        pd.DataFrame(merged_records)
        .drop(columns=["delta", "merge"])
        .reset_index(drop=True)
    )


def parse_transcript(transcript_file):
    dff = (
        pd.read_csv(transcript_file)
        # round, calculate deltas
        .assign(start=lambda x: round(x.start, 2))
        .assign(end=lambda x: round(x.end, 2))
        .assign(delta=lambda x: x.start.shift(-1) - x.end)
        .assign(merge=lambda x: x.delta > merge_threshold)
    )
    return merge_adjacent_utterances(dff)


def estimate_cost_of_ingest(transcript_df):
    ada_cost_per_1000_tokens = 0.0004
    n_tokens = len([e for e in "".join(transcript_df.text.tolist()).split(" ") if e])
    print(f"{n_tokens} tokens found in transcript")
    cost_estimate = (n_tokens / 1000) * ada_cost_per_1000_tokens
    print(f"Estimate ingestion cost: US ${cost_estimate}")


def ingest_transcript_df(transcript_df):
    # TODO: add upsert, prevent redundant writes
    documents = DataFrameLoader(
        transcript_df.head(20), page_content_column=transcript_col
    ).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    # embed, write to chroma, save chroma db
    vectordb.add_documents(texts)
    vectordb.persist()


if __name__ == "__main__":
    for transcript in list(transcript_dir.rglob("*/*.csv")):
        transcript_df = parse_transcript(transcript).assign(
            podcast=transcript.parent.name
        )
        print(f"Ingesting transcript: {transcript.name}")
        estimate_cost_of_ingest(transcript_df)
        ingest_transcript_df(transcript_df)
