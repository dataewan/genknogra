from .. import config
import os
import glob
import bz2
from xml.etree.cElementTree import iterparse
import logging
import re
import random
import pickle
import wikitextparser as wtp
from gensim.corpora import wikicorpus
from nltk import tokenize

logging.basicConfig(level=config.loglevel)
LINK_RE = re.compile("\[\[(.*?)\]\]")
NUMBER_CHARACTERS_IN_LINK_NO_DESC = 4
NUMBER_CHARACTERS_IN_LINK_WITH_DESC = 5

def findwikifiles():
    return glob.glob(os.path.join(config.datadir, "*bz2"))


def get_namespace(tag):
    """Get the namespace from the tag.
    """
    m = re.match("^{(.*?)}", tag)
    namespace = m.group(1) if m else ""
    return namespace


def process_file(filename):
    """Process bz2 compressed xml wikipedia dump

    Args:
        filename (string): File to process

    """
    logging.info(f"Processing {filename}")
    f = bz2.BZ2File(filename)
    elems = (elem for _, elem in iterparse(f, events=("end",)))
    elem = next(elems)

    namespace = get_namespace(elem.tag)
    page_tag = f"{{{namespace}}}page"
    title_path = f"{{{namespace}}}title"
    ns_path = f"{{{namespace}}}ns"
    revision_path = f"{{{namespace}}}revision"
    text_path = f"{{{namespace}}}text"
    id_path = f"{{{namespace}}}id"

    i = 0
    for elem in elems:
        if elem.tag == page_tag:
            title = elem.find(title_path).text
            revision = elem.find(revision_path)
            ns = elem.find(ns_path).text
            text = revision.find(text_path).text
            pageid = elem.find(id_path).text

            yield title, pageid, text
            elem.clear()


def export_test_set(title, pageid, text):
    logging.info(f"Exporting {title} in test set")
    with open(f"test_set/{pageid}.pkl", "wb") as f:
        pickle.dump({"title": title, "pageid": pageid, "text": text}, f)


def strip_link(sentence):
    """Strip the first link from the sentence.

    Args:
        sentence (str): sentence to remove a link from

    Returns:
        did_contain_link (bool): did this contain a link
        stripped (str): sentence with the first link markup removed
        link_page (str): the page being linked to
        span_start (int): the index in stripped where the description starts
        span_end (int): the index in stripped where the description ends
    

    """
    re_search = LINK_RE.search(sentence)
    if re_search:
        match = re_search.group()[2:-2]
        if "|" in match:
            page, description = match.split("|")
            length_removed = len(page) + NUMBER_CHARACTERS_IN_LINK_WITH_DESC
        else:
            page, description = match, match
            length_removed = NUMBER_CHARACTERS_IN_LINK_NO_DESC
        start, end = re_search.span()
        stripped = sentence[:start] + description + sentence[end:]
        return True, stripped, page, start, end - length_removed
    else:
        return False, sentence, None, None, None


def get_wikilinks(sentence):
    """Find where the links are in the sentence, remove the markup but record where the link was.

    Args:
        sentence (str): input sentence

    Returns:    
        stripped_sentence (str): sentence with the markup removed
        link_pages list(str): the page being linked to
        span_starts list(int): index of where the link description text starts
        span_ends list(int): index of where the link description text ends
    """
    link_pages = []
    span_starts = []
    span_ends = []
    did_contain_link, stripped, link_page, span_start, span_end = strip_link(sentence)

    while did_contain_link:
        link_pages += [link_page]
        span_starts += [span_start]
        span_ends += [span_end]
        did_contain_link, stripped, link_page, span_start, span_end = strip_link(
            stripped
        )

    return stripped, link_pages, span_starts, span_ends


def extract_links(title, pageid, text):
    """Extract all inter-wiki links from the text. Along with the surrounding sentences.

    Args:
        title (str): Title of the page
        pageid (str): page ID
        text (str): text to process

    Returns: TODO

    """
    sections = wtp.parse(text).sections
    for section in sections:
        text = wikicorpus.remove_markup(
            section, promote_remaining=False, simplify_links=False
        )
        sentences = tokenize.sent_tokenize(text)


def main():
    wikifiles = findwikifiles()
    p = 0.001

    for title, pageid, text in process_file(wikifiles[0]):
        if random.random() < p:
            export_test_set(title, pageid, text)
