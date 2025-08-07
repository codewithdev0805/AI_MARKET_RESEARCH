from flask import Flask, request, jsonify

app = Flask(__name__)

TRENDS = {
    "technology": ["AI", "Quantum Computing", "Blockchain"],
    "fashion": ["Vintage", "Minimalism", "Athleisure"]
}

@app.route("/list-tools", methods=["GET"])
def list_tools():
    return jsonify({"tools": [{"name": "get_trends", "parameters": {"category": "string"}}]})

@app.route("/call-tool", methods=["POST"])
def call_tool():
    data = request.json
    if data["name"] == "get_trends":
        category = data["parameters"].get("category", "technology")
        return jsonify({"trends": TRENDS.get(category, [])})
    return jsonify({"error": "Unknown tool"}), 400

import requests
from bs4 import BeautifulSoup

def fetch_market_trends(keyword):
    url = f"https://www.google.com/search?q={keyword}+market+trends"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    snippets = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')[:5]  # top 5

    trends = [s.get_text() for s in snippets]
    return trends

if __name__ == "__main__":
    keyword = "AI startups"
    results = fetch_market_trends(keyword)

    with open("ai-market-research/raw_trends.txt", "w", encoding='utf-8') as f:
        for trend in results:
            f.write(f"{trend}\n")

    print("✅ Market trends saved to raw_trends.txt")


if __name__ == "__main__":
    app.run(port=5001)
