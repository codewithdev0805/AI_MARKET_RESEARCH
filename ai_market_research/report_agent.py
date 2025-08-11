import os
import streamlit as st
from groq import Groq
from fpdf import FPDF

# Load API key and model from secrets (or env fallback)
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
model_name = st.secrets.get("GROQ_MODEL", "llama-3.3-70b-versatile")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in Streamlit secrets or environment variables.")

client = Groq(api_key=api_key)

def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Strategy file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        strategy = f.read()

    system_prompt = "You are a market research analyst. Summarize this for a professional business report."

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": strategy}
        ]
    )

    return response.choices[0].message.content.strip()

class PDF(FPDF):
    def header(self):
        self.set_fill_color(30, 144, 255)  # Blue header
        self.rect(0, 0, 210, 20, "F")
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "Market Research Report", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(summary, output_path):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 10, summary.encode("latin-1", "replace").decode("latin-1"))
    pdf.output(output_path)

def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    os.makedirs("ai-market-research", exist_ok=True)
    with open("ai-market-research/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    generate_pdf(summary, "ai-market-research/final_report.pdf")
    print("✅ Final report saved to ai-market-research/final_report.pdf")
