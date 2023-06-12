import time
from pathlib import Path

import pandas as pd
import torch
from faster_whisper import WhisperModel

from utils import logger

MODEL_SIZE = "small"
NUM_WORKERS = 16
COMPUTE_TYPE = "int8"
DATA_DIR = Path(__file__).parents[0] / "data"
PODCAST_DIR = DATA_DIR / "audio"
TRANSCRIPT_DIR = DATA_DIR / "transcripts"

device = "cuda" if bool(torch.cuda.is_available()) else "cpu"
podcasts = list(PODCAST_DIR.rglob("*/*.mp3"))
model = WhisperModel(
    MODEL_SIZE, device=device, num_workers=NUM_WORKERS, compute_type=COMPUTE_TYPE
)


def transcribe_audio(audio_file):
    audio_file = Path(audio_file)
    segments, info = model.transcribe(str(audio_file), beam_size=5)
    transcript = [
        {"start": segment.start, "end": segment.end, "text": segment.text}
        for segment in segments
    ]
    return pd.DataFrame(transcript)


def snake_case_string(string):
    return string.lower().replace(" ", "_")


if __name__ == "__main__":
    for podcast in podcasts:
        start = time.time()
        file_name = snake_case_string(podcast.name.replace(".mp3", ".csv"))
        save_name = TRANSCRIPT_DIR / podcast.parent.name / file_name

        if not save_name.parent.exists():
            save_name.parent.mkdir(parents=True, exist_ok=True)

        if save_name.exists():
            continue

        try:
            transcription = transcribe_audio(podcast)
            transcription.to_csv(save_name, index=False)
            end = time.time()
            logger.info(f"Transcribed {podcast.name} in {end - start} seconds")
        except Exception:
            logger.error(f"Could not transcribe: {podcast.name}")
