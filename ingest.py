import pandas as pd
from dotenv import load_dotenv

from config import TRANSCRIPT_DIR
from utils import logger
from vectore_store import chroma
# from vectore_store.chroma import ingest_transcript_df_chromadb

load_dotenv()
TRANSCRIPT_COL = "text"
MERGE_THRESHOLD = 1
ADA_COST_PER_1000_TOKENS = 0.0004

def merge_adjacent_utterances(df):
    dff = (
        df.assign(start_shift=lambda x: x.start.shift(-1))
        .assign(delta=lambda x: x.start_shift - x.end)
        .assign(group=lambda x: (x.delta > MERGE_THRESHOLD).cumsum())
        .groupby("group")
        .agg({"start": "min", "end": "max", "text": "".join})
        .reset_index(drop=True)
    )
    logger.info(f"Reducing {len(df)} records to {len(dff)}")
    return dff


def estimate_cost_of_ingest(transcript_df):
    n_tokens = len([e for e in "".join(transcript_df.text.tolist()).split(" ") if e])
    logger.info(f"{n_tokens} tokens found in transcript")
    cost_estimate = (n_tokens / 1000) * ADA_COST_PER_1000_TOKENS
    logger.info(f"Estimate ingestion cost: US ${cost_estimate}")


if __name__ == "__main__":
    for transcript in list(TRANSCRIPT_DIR.rglob("*/*.csv")):
        print(transcript)
        df = (
            pd.read_csv(transcript)
            .assign(start=lambda x: round(x.start, 2))
            .assign(end=lambda x: round(x.end, 2))
            .sort_values(["start", "end"])
        )
        transcript_df = (
            merge_adjacent_utterances(df)
            .assign(podcast=transcript.parent.name)
            .assign(episode=transcript.stem)
        )
        logger.info(f"Ingesting transcript: {transcript.name}")
        estimate_cost_of_ingest(transcript_df)
        chroma.ingest_transcript_df_chromadb(transcript_df, transcript_col=TRANSCRIPT_COL)
