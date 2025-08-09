import os
import requests
from flask import Flask, request, jsonify

# ✅ Try to load Groq API key from Streamlit secrets or fallback to env
try:
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

# ✅ Safety check
if not api_key:
    raise ValueError(" GROQ_API_KEY not found in Streamlit secrets or environment variables.")

# ✅ Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# 🧠 Summarize strategy using LLaMA 3 via Groq API
def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Strategy file not found: {file_path}")

    with open(file_path, "r", encoding='utf-8') as f:
        strategy = f.read()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",  # You can also use "llama3-70b-8192" if needed
        "messages": [
            {"role": "system", "content": "You are a market research analyst. Summarize this for a business report."},
            {"role": "user", "content": strategy}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Groq API error: {response.status_code} - {response.text}")

    return response.json()["choices"][0]["message"]["content"].strip()

# ✅ Function to be called from app.py
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    output_path = "ai-market-research/summary.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding='utf-8') as f:
        f.write(summary)

    print("✅ Final report saved to summary.txt")

# ✅ Optional Flask app for local microservice use
app = Flask(__name__)

@app.route("/report", methods=["POST"])
def generate_report():
    insights = request.json.get("insights", "")

    response = requests.post("http://localhost:5002/call-tool", json={
        "name": "generate_pdf",
        "parameters": {"insights": insights}
    })

    return jsonify(response.json())
