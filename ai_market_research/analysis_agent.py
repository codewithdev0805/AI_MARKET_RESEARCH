from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# === SMART ANALYST AGENT ===
def analyst_agent(raw_data, keyword=None):
    print("🔍 Analyst Agent: Interpreting raw market trends...")

    # Handle keyword enrichment
    if keyword:
        filtered = [line for line in raw_data if keyword.lower() in line.lower()]
        if not filtered:
            # Fallback: no direct matches
            filtered = [f"No direct trend mentions of '{keyword}'. Please infer insights related to it."]
        else:
            # Add context prefix
            filtered = [f"Keyword: {keyword}"] + filtered
    else:
        filtered = raw_data

    # Simulate interpretation (replace with OpenAI later)
    return [f"Insight: {line.strip().upper()}" for line in filtered]


# === SMART STRATEGIST AGENT ===
def strategist_agent(insights):
    print("🧠 Strategist Agent: Generating business recommendations...")
    # Simulate recommendations
    return [f"📈 Opportunity: Based on {insight}" for insight in insights]


# === MAIN FUNCTION FOR AGENT RUN ===
def run_analysis_agent(keyword):
    print(f"⚙️ Running analysis agent for keyword: {keyword}")

    # Save keyword
    with open("ai-market-research/selected_keyword.txt", "w", encoding='utf-8') as f:
        f.write(keyword)

    # Read raw market trends
    with open("ai-market-research/raw_trends.txt", "r", encoding='utf-8') as f:
        raw = f.readlines()

    # Run both agents
    insights = analyst_agent(raw, keyword=keyword)
    strategy = strategist_agent(insights)

    # Save strategy
    with open("ai-market-research/strategy.txt", "w", encoding='utf-8') as f:
        for item in strategy:
            f.write(f"{item}\n")

    print("✅ Strategy recommendations saved to strategy.txt")
    return strategy


# === FLASK API ENDPOINT ===
@app.route("/analyze", methods=["POST"])
def analyze():
    payload = request.json
    keyword = payload.get("keyword", "")
    data = payload.get("data", [])

    insights = analyst_agent(data, keyword=keyword)
    strategy = strategist_agent(insights)

    print("✅ Insights generated:", strategy)

    # Forward insights to report agent (PDF tool)
    requests.post("http://localhost:7001/report", json={"insights": strategy})

    return jsonify({"insights": strategy})


# === RUN LOCAL SERVER ===
if __name__ == "__main__":
    app.run(port=6001)
