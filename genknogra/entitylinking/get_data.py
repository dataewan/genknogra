import sys
import json
import requests
import logging
from tqdm import tqdm
import os
from .. import config

logging.basicConfig(level=config.loglevel)
BASE_URL = "https://dumps.wikimedia.org/"


def get_json(json_url):
    logging.info("Getting JSON of file descriptors")
    r = requests.get(json_url)
    return json.loads(r.text)


def get_filedescriptors(wiki_json):
    return wiki_json["jobs"]["articlesmultistreamdump"]["files"]


def filter_sort_keys(file_descriptors):
    keys = list(file_descriptors.keys())
    return sorted(filter(lambda x: "index" not in x, keys))


def download_file(key, file_descriptor):
    url = BASE_URL + file_descriptor.get("url")
    logging.info(f"Downloading {url}")
    r = requests.get(url, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    t = tqdm(total = total_size, unit="iB", unit_scale=True)
    outfilename = os.path.join(config.datadir, key)
    with open(outfilename, "wb") as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()


def get_files(wiki_json):
    file_descriptors = get_filedescriptors(wiki_json)
    sorted_relevant_keys = filter_sort_keys(file_descriptors)
    for key in sorted_relevant_keys:
        download_file(key, file_descriptors[key])


def main(json_url):
    wiki_json = get_json(json_url)
    get_files(wiki_json)
