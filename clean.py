import re
import spacy
from urllib.parse import urlparse

nlp = spacy.load("en_core_web_sm")
def clean_url(url):
    parsed = urlparse(url)
    path = re.sub(r"/$", "", parsed.path)
    doc = nlp(path)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return "/" + "/".join(tokens)

with open("crawled_urls.txt", "r") as f:
    urls = f.read().splitlines()

cleaned_urls = [clean_url(url) for url in urls]
with open("cleaned_urls.txt", "w") as f:
    for url in cleaned_urls:
        f.write(url + "\n")
