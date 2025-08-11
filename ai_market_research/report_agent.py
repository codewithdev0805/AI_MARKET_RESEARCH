import os
import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
from groq import Groq

# ---------- Load API Key & Model Name ----------
try:
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
    model_name = st.secrets.get("MODEL_NAME", "llama-3.3-70b-versatile")
except:
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

if not api_key:
    raise ValueError("❌ API key not found.")

client = Groq(api_key=api_key)

# ---------- AI Summarization ----------
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

# ---------- PDF Class ----------
class PDF(FPDF):
    def header(self):
        self.set_fill_color(41, 128, 185)  # Blue header
        self.rect(0, 0, 210, 25, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 12, "Market Research Report", ln=True, align="C")
        self.set_font("Helvetica", "", 12)
        self.cell(0, 8, datetime.date.today().strftime("%B %d, %Y"), ln=True, align="C")
        self.ln(10)

    def section_title(self, title, icon_path=None):
        self.set_text_color(41, 128, 185)
        self.set_font("Helvetica", "B", 14)
        if icon_path and os.path.exists(icon_path):
            self.image(icon_path, x=self.get_x(), y=self.get_y(), w=8)
            self.cell(10)  # Move right
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def section_body(self, text):
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, text)
        self.ln()

# ---------- Chart Creation ----------
def create_trend_chart(data, output_path):
    plt.figure(figsize=(6, 3))
    bars = plt.bar(data.keys(), data.values(), color="#2980b9")
    plt.xticks(rotation=45, ha='right')
    plt.title("Keyword Trend Frequency", fontsize=14, color="#2980b9")
    plt.tight_layout()
    # Label bars
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), str(bar.get_height()),
                 ha='center', va='bottom', fontsize=10)
    plt.savefig(output_path, dpi=300)
    plt.close()

# ---------- PDF Generation ----------
def generate_pdf(summary_text, trend_data, output_path):
    pdf = PDF()
    pdf.add_page()

    # Executive Summary Section
    pdf.section_title("Executive Summary", icon_path="ai-market-research/icons/summary.png")
    pdf.section_body(summary_text)

    # Trend Analysis Section
    if trend_data:
        chart_path = "ai-market-research/trend_chart.png"
        create_trend_chart(trend_data, chart_path)
        pdf.section_title("Trend Analysis", icon_path="ai-market-research/icons/chart.png")
        pdf.image(chart_path, x=10, w=180)

    # Optional Branding / Footer Image
    branding_path = "ai-market-research/icons/footer.png"
    if os.path.exists(branding_path):
        pdf.ln(10)
        pdf.image(branding_path, x=60, w=90)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path, "F")

# ---------- Main Function ----------
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    # Load trend data if available
    trend_data = {}
    trends_file = "ai-market-research/raw_trends.txt"
    if os.path.exists(trends_file):
        with open(trends_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    trend_data[parts[0].strip()] = int(parts[1].strip())

    generate_pdf(summary, trend_data, "ai-market-research/final_report.pdf")
    print("✅ Final report saved to final_report.pdf")
