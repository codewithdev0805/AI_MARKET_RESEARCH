import os
import streamlit as st
from fpdf import FPDF
from groq import Groq

# ✅ Load API key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]

# ✅ Initialize Groq client
client = Groq(api_key=api_key)

# 🧠 Summarize strategy using Groq's updated LLaMA model
def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ strategy file not found: {file_path}")

    with open(file_path, "r", encoding='utf-8') as f:
        strategy = f.read()

    system_prompt = (
        "You are a market research analyst. Summarize the following content for a professional business report. "
        "Keep it concise, structured with bullet points, and relevant only to the given topic."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-specdec",  # ✅ Updated model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": strategy}
        ]
    )

    return response.choices[0].message.content.strip()

# 📄 PDF Generator with nice formatting
class PDF(FPDF):
    def header(self):
        # Blue header box
        self.set_fill_color(30, 144, 255)  # Dodger blue
        self.rect(0, 0, 210, 20, 'F')
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "AI Market Research Report", ln=True, align="C")

    def chapter_title(self, title):
        self.ln(8)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 144, 255)
        self.multi_cell(0, 8, title)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font("Helvetica", "", 12)
        self.set_text_color(0, 0, 0)
        safe_body = body.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, safe_body)
        self.ln()

def generate_pdf(summary_text, output_path):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add content
    pdf.chapter_title("Market Research Summary")
    pdf.chapter_body(summary_text)

    pdf.output(output_path)
    print(f"✅ PDF saved to {output_path}")

# ✅ Main function to be called from app.py
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    output_path = "ai-market-research/summary.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding='utf-8') as f:
        f.write(summary)

    generate_pdf(summary, "ai-market-research/final_report.pdf")
    print("✅ Final report saved to summary.txt & final_report.pdf")
