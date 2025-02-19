# Property Oracle 🏠

AI-powered chat interface for Australian property insights using podcast transcripts. Companion code for ["Property Oracle"](https://www.samhardyhey.com/property-oracle).

## Features
- 🎙️ Property podcast collection
- 📝 Audio transcription
- 🧠 Vector store integration
- 💬 Interactive chat interface

## Setup
```bash
# Install dependencies
./scripts/create_env.sh
```

## Usage
```bash
# Download property podcasts
python property_oracle/data/podcast.py

# Generate transcripts
python property_oracle/data/transcript.py

# Build vector store
python property_oracle/data/ingest.py

# Launch chat interface
python property_oracle/main.py
```

## Structure
- 🎧 `data/podcast.py` # Podcast retrieval
- 📄 `data/transcript.py` # Transcription
- 💾 `data/ingest.py` # Vector store creation
- 🤖 `main.py` # Chat application

*Note: Requires OpenAI API key and sufficient compute for transcription.*