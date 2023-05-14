import re
import string
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests
from srsly import read_json


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


def snake_case_string(s):
    # Remove punctuation
    s = s.translate(str.maketrans("", "", string.punctuation))

    # Lowercase
    s = s.lower()

    # Replace spaces (and possibly multiple spaces) with underscores
    s = re.sub(" +", "_", s)

    return s


# Function to download one file
def download_file(url, title, directory):
    try:
        response = requests.get(url)
        file_path = directory / f"{title}.mp3"
        with open(str(file_path), "wb") as f:
            f.write(response.content)
        print(f"Successfully downloaded {url}")
    except Exception:
        print(f"Error downloading {url}")


if __name__ == "__main__":
    podcasts = read_json("/Users/samhardyhey/.podcast_downloader_config.json")["podcasts"]

    # create directories
    meta_dir = Path("./data/meta/")
    if not meta_dir.exists():
        meta_dir.mkdir(parents=True, exist_ok=True)
    audio_dir = Path("./data/audio/")
    if not audio_dir.exists():
        audio_dir.mkdir(parents=True, exist_ok=True)

    for podcast in podcasts:
        # fetch/format metadata
        print(f"Retrieving XML feed for: {podcast['name']}")
        res = requests.get(podcast["rss_link"])
        xml_dict = parse_xml_objects(res.text)
        meta_df = format_xml_objects(xml_dict).assign(title=lambda x: x.title.apply(snake_case_string))
        meta_file_save = meta_dir / f"{snake_case_string(podcast['name'])}.csv"
        print(f"Saving meta data to: {meta_file_save}, found {len(meta_df)} episodes")
        meta_df.to_csv(meta_file_save, index=False)

        audio_download_dir = Path("./data/audio") / snake_case_string(podcast["name"])
        if not audio_download_dir.exists():
            audio_download_dir.mkdir(parents=True, exist_ok=True)

        # parallelize the downloads
        with ThreadPoolExecutor(max_workers=12) as executor:
            tasks = [(record.url, record.title, audio_download_dir) for idx, record in meta_df.head(10).iterrows()]
            list(executor.map(lambda params: download_file(*params), tasks))
