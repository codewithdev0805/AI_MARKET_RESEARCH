import os
import requests
from flask import Flask, request, jsonify
from fpdf import FPDF

# ✅ Load Groq API key
try:
    import streamlit as st
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in secrets or environment variables.")

# 🧠 Summarize using Groq
def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Strategy file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        strategy = f.read()

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a professional market research analyst. Summarize this for a polished, concise business report with key points clearly outlined."},
            {"role": "user", "content": strategy}
        ],
        "max_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"].strip()

# 🎨 Pretty PDF with header box & images
class PDF(FPDF):
    def header(self):
        # Blue header box
        self.set_fill_color(0, 102, 204)
        self.rect(0, 0, 210, 25, 'F')

        # Logo if exists
        if os.path.exists("logo.png"):
            self.image("logo.png", 10, 5, 20)

        # Title
        self.set_text_color(255, 255, 255)
        self.set_font("DejaVu", "B", 18)
        self.cell(0, 15, "AI-Powered Market Research Report", ln=True, align="C")

        self.ln(10)

    def chapter_title(self, title):
        self.set_font("DejaVu", "B", 14)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font("DejaVu", "", 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8, body)
        self.ln()

    def add_section_image(self, image_path):
        if os.path.exists(image_path):
            self.image(image_path, x=10, w=190)
            self.ln(5)

# 📄 Generate PDF
def generate_pdf(summary_text, output_path):
    pdf = PDF()

    # Load DejaVu font for Unicode
    try:
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.add_font("DejaVu", "B", "DejaVuSans.ttf", uni=True)
    except:
        print("⚠️ Font not found. Using default Helvetica.")
        pdf.set_font("Helvetica", "", 12)

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Optional cover image
    if os.path.exists("cover.jpg"):
        pdf.add_section_image("cover.jpg")

    pdf.chapter_title("Executive Summary")
    pdf.chapter_body(summary_text)

    # Optional chart/graphic
    if os.path.exists("chart.png"):
        pdf.chapter_title("Market Trends")
        pdf.add_section_image("chart.png")

    pdf.output(output_path)
    print(f"✅ PDF report generated: {output_path}")

# 🚀 Main pipeline
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    # Save text
    os.makedirs("ai-market-research", exist_ok=True)
    with open("ai-market-research/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("✅ Summary saved to summary.txt")

    # Save PDF
    generate_pdf(summary, "ai-market-research/final_report.pdf")

# 🌐 Optional Flask route
app = Flask(__name__)

@app.route("/report", methods=["POST"])
def generate_report():
    insights = request.json.get("insights", "")
    generate_pdf(insights, "ai-market-research/final_report.pdf")
    return jsonify({"status": "success", "message": "PDF generated."})
