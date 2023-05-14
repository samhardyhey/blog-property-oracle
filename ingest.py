import pandas as pd
from dotenv import load_dotenv

from transcribe import transcript_dir

load_dotenv()
transcript_col = "text"
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


if __name__ == "__main__":
    for transcript in list(transcript_dir.rglob("*/*.csv")):
        transcript_df = (
            parse_transcript(transcript)
            .assign(podcast=transcript.parent.name)
            .assign(episode=transcript.stem)
            # for QA with sources
            .assign(
                source=lambda x: x.apply(
                    lambda y: f"{y.podcast} | {y.episode} | {y.start} | {y.end}", axis=1
                )
            )
        )
        print(f"Ingesting transcript: {transcript.name}")
        estimate_cost_of_ingest(transcript_df)
        ingest_transcript_df(transcript_df)
