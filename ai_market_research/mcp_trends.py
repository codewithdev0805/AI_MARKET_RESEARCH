from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

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


def run_mcp_trends(keyword):
    print(f"🔎 Fetching market trends for: {keyword}")
    
    url = f"https://www.google.com/search?q={keyword}+market+trends"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    snippets = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')[:5]

    trends = [s.get_text() for s in snippets]

    if not trends:
        print("⚠️ No trends found. Possibly blocked by Google.")
    else:
        output_dir = "ai-market-research"
        os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/raw_trends.txt", "w", encoding='utf-8') as f:
            for trend in trends:
                f.write(f"{trend}\n")
        print("✅ Trends saved to raw_trends.txt")

    return trends


if __name__ == "__main__":
    # Example test mode: Run trend fetcher manually
    keyword = "AI startups"
    run_mcp_trends(keyword)

    # Run the Flask API server
    app.run(port=5001)

