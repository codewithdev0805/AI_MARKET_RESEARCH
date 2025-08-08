import os
import requests
from flask import Flask, request, jsonify
from openai import OpenAI

# ✅ Try to load from Streamlit secrets if available (only inside Streamlit app)
try:
    import streamlit as st
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = os.getenv("OPENAI_API_KEY")  # fallback for local dev or Flask server

# ✅ Initialize OpenAI client
client = OpenAI(api_key=api_key)

# 🧠 Summarize strategy using OpenAI
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

# ✅ Function to be called from app.py
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    with open("ai-market-research/summary.txt", "w", encoding='utf-8') as f:
        f.write(summary)

    print("✅ Final report saved to summary.txt")

# Optional: Run Flask server locally (if needed)
app = Flask(__name__)

@app.route("/report", methods=["POST"])
def generate_report():
    insights = request.json["insights"]

    response = requests.post("http://localhost:5002/call-tool", json={
        "name": "generate_pdf",
        "parameters": {"insights": insights}
    })

    return jsonify(response.json())
