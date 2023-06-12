import multiprocessing
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

from config import META_DIR, PODCAST_DIR
from utils import logger, snake_case_string

PODCAST_META = [
    {
        "name": "Your First Home Buyer Guide Podcast",
        "rss_link": "https://www.omnycontent.com/d/playlist/3c72444b-621f-4a3e-b6e1-a82000673c2f/52a142e1-0905-48a3-9586-ac91001d6222/e3f25be2-d0d8-4aae-a501-ac91002373ff/podcast.rss",
    },
    {
        "name": "My Millenial Property",
        "rss_link": "https://feeds.acast.com/public/shows/62fa0d8926f5af001280299c",
    },
    {
        "name": "Your Strata Property",
        "rss_link": "https://www.yourstrataproperty.com.au/feed/podcast/",
    },
    {
        "name": "The Home Run",
        "rss_link": "https://omny.fm/shows/the-home-run/playlists/podcast.rss",
    },
    {
        "name": "The Elephant in the Room Property Podcast",
        "rss_link": "https://www.omnycontent.com/d/playlist/3c72444b-621f-4a3e-b6e1-a82000673c2f/469eaf17-e0b5-4a92-94c3-ad8e001a1506/92ba93e7-629e-4c65-bffa-ad8e001a151e/podcast.rss",
    },
    {
        "name": "Australian Property Podcast",
        "rss_link": "https://feeds.megaphone.fm/australian-property-podcast",
    },
]

MAX_DOWNLOAD_WORKERS = 16
NUM_CORES = multiprocessing.cpu_count()


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = {}
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                try:
                    dd[k].append(v)
                except KeyError:
                    dd[k] = [v]
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update((f"@{k}", v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]["#text"] = text
        else:
            d[t.tag] = text
    return d


def parse_xml_objects(xml_string):
    root = ET.ElementTree(ET.fromstring(xml_string)).getroot()
    return etree_to_dict(root)


def format_xml_objects(xml_dict):
    return (
        pd.DataFrame(xml_dict["rss"]["channel"]["item"])
        .pipe(lambda x: x[["title", "pubDate", "enclosure", "link", "description"]])
        .assign(enclosure=lambda x: x.enclosure.apply(lambda y: y["@url"]))
        .rename(columns={"enclosure": "url"})
    )

def download_file(url, title, directory):
    try:
        response = requests.get(url)
        file_path = directory / f"{title}.mp3"
        with open(str(file_path), "wb") as f:
            f.write(response.content)
        logger.info(f"Successfully downloaded {url}")
    except Exception:
        logger.warning(f"Error downloading {url}")


def retrieve_podcasts():
    # create output dirs
    if not META_DIR.exists():
        META_DIR.mkdir(parents=True, exist_ok=True)
    if not PODCAST_DIR.exists():
        PODCAST_DIR.mkdir(parents=True, exist_ok=True)

    for podcast in PODCAST_META:
        # fetch/format metadata
        logger.info(f"Retrieving XML feed for: {podcast['name']}")
        res = requests.get(podcast["rss_link"])
        xml_dict = parse_xml_objects(res.text)
        meta_df = format_xml_objects(xml_dict).assign(
            title=lambda x: x.title.apply(snake_case_string)
        )
        meta_file_save = META_DIR / f"{snake_case_string(podcast['name'])}.csv"
        logger.info(
            f"Saving meta data to: {meta_file_save}, found {len(meta_df)} episodes"
        )
        meta_df.to_csv(meta_file_save, index=False)

        audio_download_dir = PODCAST_DIR / snake_case_string(podcast["name"])
        if not audio_download_dir.exists():
            audio_download_dir.mkdir(parents=True, exist_ok=True)

        # parallelize the downloads
        with ThreadPoolExecutor(max_workers=NUM_CORES) as executor:
            tasks = [
                (record.url, record.title, audio_download_dir)
                for idx, record in meta_df.iterrows()
            ]
            list(executor.map(lambda params: download_file(*params), tasks))

if __name__ == "__main__":
    retrieve_podcasts()