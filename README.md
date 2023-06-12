## Blog Property Oracle
Notebooks and scripts for the:

- Retrieval of Podcasts, naturally focused on Australian Property
- Transcribing of podcasts
- Ingesting podcast transcripts into a vector store (chroma by default)
- Small/basic chat application for interacting with the vector store

See the accompanying blog post [here](https://www.samhardyhey.com/).

## Install
- via `scripts/create_env.sh`

## Usage
- **Podcast retrieval.** Via `python property_oracle/data/podcast.py`
- **Podcast transcription.** Via ``python property_oracle/data/transcript.py``
- **Transcript ingestion.** Via ``python property_oracle/data/ingest.py``
- **Property Oracle Chat.** Via ``python property_oracle/main.py``

All code obviously dependant upon configuring an openAI API key and some decent hardware to transcribe the podcasts with.