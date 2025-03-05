import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

start_url = "https://example.com"
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
            print("Found:", link)
            queue.append(link)

with open("crawled_urls.txt", "w") as f:
    for url in visited:
        f.write(url + "\n")
