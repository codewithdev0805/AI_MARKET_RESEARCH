import os
import requests
from flask import Flask, request, jsonify
import google.generativeai as genai

# ✅ Try to load API key from Streamlit secrets or fallback to environment variable
try:
    import streamlit as st
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(" GEMINI_API_KEY not found in Streamlit secrets or environment variables.")

# ✅ Configure Gemini
genai.configure(api_key=api_key)

# 🧠 Summarize strategy using Gemini
def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ strategy file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        strategy = f.read()

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"You are a market research analyst. Summarize this for a business report:\n\n{strategy}")
    return response.text.strip()

# ✅ Function to be called from app.py
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    output_path = "ai-market-research/summary.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
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
