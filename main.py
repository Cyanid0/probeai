import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import spacy
import subprocess

def crawl(start_url):
    domain = urlparse(start_url).netloc
    visited = set()
    queue = [start_url]
    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            r = requests.get(url)
        except:
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])
            if urlparse(link).netloc == domain and link not in visited:
                queue.append(link)
    with open("crawled_urls.txt", "w") as f:
        for url in visited:
            f.write(url + "\n")
    print("Crawled URLs saved to crawled_urls.txt")

def clean_data():
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
    print("Cleaned URLs saved to cleaned_urls.txt")

def predict_endpoints():
    with open("cleaned_urls.txt", "r") as f:
        urls = f.read()
    prompt = "Based on these crawled URLs, suggest additional potential endpoints or directories that might exist on the website:\n" + urls
    result = subprocess.run(["ollama", "query", "model-name", prompt], capture_output=True, text=True)
    print(result.stdout)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    crawl_parser = subparsers.add_parser("crawl")
    crawl_parser.add_argument("url")
    subparsers.add_parser("clean")
    subparsers.add_parser("predict")
    args = parser.parse_args()
    if args.command == "crawl":
        crawl(args.url)
    elif args.command == "clean":
        clean_data()
    elif args.command == "predict":
        predict_endpoints()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
