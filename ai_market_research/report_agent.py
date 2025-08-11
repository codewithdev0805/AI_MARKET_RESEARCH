import os
import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
from groq import Groq

# ✅ Load API key & model name from secrets or env
try:
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
    model_name = st.secrets.get("MODEL_NAME", "llama-3.3-70b-versatile")
except:
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

if not api_key:
    raise ValueError("❌ API key not found. Set GROQ_API_KEY in Streamlit secrets or env variables.")

# ✅ Initialize Groq client
client = Groq(api_key=api_key)

# ---------- AI SUMMARIZATION ----------
def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Strategy file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        strategy = f.read()

    prompt = f"You are a market research analyst. Summarize this for a polished, professional business report:\n\n{strategy}"

    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

# ---------- PDF DESIGN ----------
class PDF(FPDF):
    def header(self):
        # Blue banner
        self.set_fill_color(41, 128, 185)
        self.rect(0, 0, 210, 20, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Market Research Report", ln=True, align="C")
        self.set_font("Helvetica", "", 12)
        self.cell(0, 10, datetime.date.today().strftime("%B %d, %Y"), ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_text_color(41, 128, 185)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def chapter_body(self, text):
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, text)
        self.ln()

# ---------- CHART CREATION ----------
def create_trend_chart(data, output_path):
    plt.figure(figsize=(6, 3))
    plt.bar(range(len(data)), data.values(), color="#2980b9")
    plt.xticks(range(len(data)), data.keys(), rotation=45, ha='right')
    plt.title("Keyword Trend Frequency")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

# ---------- PDF GENERATION ----------
def generate_pdf(summary_text, trend_data, output_path):
    pdf = PDF()
    pdf.add_page()

    # Summary section
    pdf.chapter_title("Executive Summary")
    pdf.chapter_body(summary_text)

    # Chart
    if trend_data:
        chart_path = "ai-market-research/trend_chart.png"
        create_trend_chart(trend_data, chart_path)
        pdf.chapter_title("Trend Analysis")
        pdf.image(chart_path, x=10, y=None, w=180)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path, "F")

# ---------- MAIN FUNCTION ----------
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    # Load trend data if available
    trend_data = {}
    trends_file = "ai-market-research/raw_trends.txt"
    if os.path.exists(trends_file):
        with open(trends_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    trend_data[parts[0].strip()] = int(parts[1].strip())

    generate_pdf(summary, trend_data, "ai-market-research/final_report.pdf")
    print("✅ Final report saved to final_report.pdf")
