import os
import requests
from flask import Flask, request, jsonify
from groq import Groq
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ✅ Try to load API key from Streamlit secrets or fallback to env
try:
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in Streamlit secrets or environment variables.")

# ✅ Initialize Groq client
client = Groq(api_key=api_key)

# 🧠 Summarize strategy using Groq
def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ strategy file not found: {file_path}")

    with open(file_path, "r", encoding='utf-8') as f:
        strategy = f.read()

    system_prompt = "You are a market research analyst. Summarize this for a business report."

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": strategy}
        ]
    )

    return response.choices[0].message.content.strip()

# 📝 Generate PDF from summary.txt
def generate_pdf_from_summary():
    summary_path = "ai-market-research/summary.txt"
    pdf_path = "ai-market-research/final_report.pdf"

    if not os.path.exists(summary_path):
        raise FileNotFoundError("❌ summary.txt not found.")

    with open(summary_path, "r", encoding="utf-8") as f:
        summary_text = f.read()

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    y_position = height - 50
    for line in summary_text.split("\n"):
        c.drawString(50, y_position, line)
        y_position -= 15
        if y_position < 50:
            c.showPage()
            y_position = height - 50

    c.save()
    print(f"✅ PDF generated at {pdf_path}")

# ✅ Function to be called from app.py
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    output_path = "ai-market-research/summary.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding='utf-8') as f:
        f.write(summary)

    print("✅ Final report saved to summary.txt")

    # Generate PDF locally
    generate_pdf_from_summary()

# Optional Flask app (if you still want API access)
app = Flask(__name__)

@app.route("/report", methods=["POST"])
def generate_report():
    insights = request.json.get("insights", "")

    # Save insights to summary and PDF
    summary_path = "ai-market-research/summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(insights)

    generate_pdf_from_summary()
    return jsonify({"message": "✅ PDF generated successfully"})
