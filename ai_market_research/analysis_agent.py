from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Set up data directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "ai-market-research")
os.makedirs(DATA_DIR, exist_ok=True)

# Agent: Interprets raw trends
def analyst_agent(trends):
    print("🔍 Analyst Agent: Interpreting raw market trends...")
    return [trend.strip().capitalize() for trend in trends if trend.strip()]

# Agent: Translates insights into business strategy
def strategist_agent(insights):
    print("🧠 Strategist Agent: Generating business recommendations...")
    return [f"Opportunity: {insight}" for insight in insights]

# Main function to run both agents
def run_analysis_agent(keyword):
    print(f"⚙️ Running analysis agent for keyword: {keyword}")

    # Save keyword
    keyword_file = os.path.join(DATA_DIR, "selected_keyword.txt")
    with open(keyword_file, "w", encoding='utf-8') as f:
        f.write(keyword)

    # Load raw trends
    DATA_DIR = "ai_market_research/ai-market-research"  # or wherever raw_trends.txt is located
    raw_path = os.path.join(DATA_DIR, "raw_trends.txt")
    with open(raw_path, "r", encoding='utf-8') as f:
        raw = f.readlines()

    # Optional: Filter raw data by keyword
    raw_filtered = [line for line in raw if keyword.lower() in line.lower()]
    if not raw_filtered:
        print("⚠️ No matching trends found for the keyword. Using full dataset.")
        raw_filtered = raw

    # Run both agents
    interpreted = analyst_agent([f"Keyword: {keyword}"] + raw_filtered)
    strategy = strategist_agent(interpreted)

    # Save strategy to file
    strategy_path = os.path.join(DATA_DIR, "strategy.txt")
    with open(strategy_path, "w", encoding='utf-8') as f:
        for item in strategy:
            f.write(f"{item}\n")

    print("✅ Strategy recommendations saved to strategy.txt")
    return strategy

# API endpoint to trigger agent
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json.get("data", [])
    keyword = request.json.get("keyword", "default")

    # Use new agents
    interpreted = analyst_agent(data)
    strategy = strategist_agent(interpreted)

    # Optional: trigger external report generation
    requests.post("http://localhost:7001/report", json={"insights": strategy})
    return jsonify({"insights": strategy})

if __name__ == "__main__":
    app.run(port=6001)
