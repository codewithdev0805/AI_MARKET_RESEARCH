import os
import requests
from bs4 import BeautifulSoup

def run_mcp_trends(keyword):
    print(f"🔎 Fetching market trends for: {keyword}")

    output_dir = "ai-market-research"
    os.makedirs(output_dir, exist_ok=True)

    # ✅ Clear old trend files before writing new data
    open(f"{output_dir}/raw_trends.txt", "w", encoding="utf-8").close()
    open(f"{output_dir}/strategy.txt", "w", encoding="utf-8").close()

    # --- Example Google Trends / News Scraper ---
    search_url = f"https://www.google.com/search?q={keyword}+market+trends"
    headers = {"User-Agent": "Mozilla/5.0"}

    resp = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    results = []
    for g in soup.select(".BNeawe.s3v9rd.AP7Wnd"):
        text = g.get_text().strip()
        if keyword.lower() in text.lower():  # ✅ filter irrelevant topics
            results.append(text)

    if not results:
        results.append(f"No specific recent trends found for {keyword}.")

    with open(f"{output_dir}/raw_trends.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"✅ Trends saved for {keyword}")
