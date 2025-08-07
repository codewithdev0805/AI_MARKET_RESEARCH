from flask import Flask, request, jsonify
import requests
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_strategy(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        strategy = f.read()

    system_prompt = "You are a market research analyst. Summarize this for a business report."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": strategy}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    summary = summarize_strategy("ai-market-research/strategy.txt")

    with open("ai-market-research/summary.txt", "w", encoding='utf-8') as f:
        f.write(summary)

    print("✅ Final report saved to summary.txt")

app = Flask(__name__)

@app.route("/report", methods=["POST"])
def generate_report():
    insights = request.json["insights"]
    response = requests.post("http://localhost:5002/call-tool", json={
        "name": "generate_pdf",
        "parameters": {"insights": insights}
    })
    result = response.json()
    print(result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=7001)
