import os
import requests
from flask import Flask, request, jsonify
from openai import OpenAI

# ✅ Try to load API key from Streamlit secrets or fallback to env
try:
    import streamlit as st
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = os.getenv("OPENAI_API_KEY")

# ✅ Log to confirm key is loaded (use only for debug, not in production)
if api_key:
    print(f"🔐 OpenAI key loaded: {api_key[:5]}...")
else:
    raise ValueError("❌ OPENAI_API_KEY not found in Streamlit secrets or environment variables.")

# ✅ Initialize OpenAI client
client = OpenAI(api_key=api_key)

# 🧠 Summarize strategy using OpenAI
def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ strategy file not found: {file_path}")

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

    return response.choices[0].message.content.strip()

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
