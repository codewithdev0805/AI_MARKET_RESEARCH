from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def analyst_agent(trends):
    print("🔍 Analyst Agent: Interpreting raw market trends...")
    return [t.strip().upper() for t in trends]

def strategist_agent(interpreted):
    print("🧠 Strategist Agent: Generating business recommendations...")
    return [f"Opportunity: {line}" for line in interpreted]

def run_analysis_agent():
    print("⚙️ Running analysis agent as a function...")

    with open("ai-market-research/raw_trends.txt", "r", encoding='utf-8') as f:
        raw = f.readlines()

    interpreted = analyst_agent(raw)
    strategy = strategist_agent(interpreted)

    with open("ai-market-research/strategy.txt", "w", encoding='utf-8') as f:
        for item in strategy:
            f.write(f"{item}\n")

    print("✅ Strategy recommendations saved to strategy.txt")
    return strategy


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json["data"]
    insights = analyst_agent(data)
    strategy = strategist_agent(insights)

    print("Insights:", strategy)
    requests.post("http://localhost:7001/report", json={"insights": strategy})
    return jsonify({"insights": strategy})

if __name__ == "__main__":
    app.run(port=6001)

