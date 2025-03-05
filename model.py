import subprocess
with open("crawled_urls.txt", "r") as f:
    urls = f.read()
prompt = "Based on these crawled URLs, suggest additional potential endpoints or directories that might exist on the website:\n" + urls
result = subprocess.run(["ollama", "query", "model-name", prompt], capture_output=True, text=True)
print(result.stdout)
