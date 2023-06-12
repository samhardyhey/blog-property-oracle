import time
from pathlib import Path

import pandas as pd
from faster_whisper import WhisperModel

model_size = "small"
# model = WhisperModel(model_size, device="cpu", num_workers=8, compute_type="int8")
model = WhisperModel(model_size, device="cuda", num_workers=16, compute_type="int8")
podcast_dir = Path("./data/audio/")
transcript_dir = Path("./data/transcripts/")
podcasts = list(podcast_dir.rglob("*/*.mp3"))


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
        save_name = transcript_dir / podcast.parent.name / file_name

        if not save_name.parent.exists():
            save_name.parent.mkdir(parents=True, exist_ok=True)

        if save_name.exists():
            continue

        try:
            transcription = transcribe_audio(podcast)
            transcription.to_csv(save_name, index=False)
            end = time.time()
            print(f"Transcribed {podcast.name} in {end - start} seconds")
        except Exception:
            print(f"Could not transcribe: {podcast.name}")
