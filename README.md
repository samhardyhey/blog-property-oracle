# TODO:
- open source alternatives for everything?
- GPU integration > S3 bucket for storage
- Hosted vector DB

## Podcast downloaders
- python module: https://github.com/dplocki/podcast-downloader
- turn a google podcast feed into an RSS feed: https://getrssfeed.com/
```python -m podcast_downloader```
- couldn't figure out how to backfill for all podcasts > wrote my own parser to generate podcast/download metadata
    - incorporates some formatting too

## Target podcasts
[my millennial property | podcast — my millennial money](https://www.mymillennial.money/my-property)
[‎Your First Home Buyer Guide Podcast on Apple Podcasts](https://podcasts.apple.com/au/podcast/your-first-home-buyer-guide-podcast/id1544701825)
[The Home Run](https://thehomerun.com.au/)
[‎The Elephant In The Room Property Podcast | Inside Australian Real Estate on Apple Podcasts](https://podcasts.apple.com/au/podcast/the-elephant-in-the-room-property-podcast/id1384822719)
[‎Australian Property Podcast on Apple Podcasts](https://podcasts.apple.com/au/podcast/australian-property-podcast/id1674727768)

- retrieve underlying RSS feed

## Whisper transcription
- faster whisper

## Vector DB
- chroma: local dev
    - difficulty upserting docs?
    - need a hosted solution eventually?

## LLM

## Storage
pip install awscli

aws configure

aws s3api create-bucket --bucket blog-property-oracle --region ap-southeast-2 --create-bucket-configuration LocationConstraint=ap-southeast-2

aws s3 sync ./data s3://blog-property-oracle/data

aws s3 sync s3://blog-property-oracle/data/transcripts/australian_property_podcast ./data/transcripts/australian_property_podcast

aws configure set default.s3.max_concurrent_requests 100
