import os
import requests
from fpdf import FPDF
import streamlit as st
from groq import Groq  # Using Groq LLaMA API

# Load Groq API key
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Summarize strategy using LLaMA from Groq
def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ strategy file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        strategy = f.read()

    prompt = f"You are a market research analyst. Summarize this for a professional business report:\n\n{strategy}"

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content.strip()

# PDF Class with Pretty Header
class PDF(FPDF):
    def header(self):
        # Blue header box
        self.set_fill_color(30, 60, 150)  # Dark blue
        self.rect(0, 0, 210, 20, "F")  # Fill top area
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, "📊 Market Research Report", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(summary_text, output_path):
    pdf = PDF()
    pdf.add_page()

    # Add image (optional)
    image_path = os.path.join(os.path.dirname(__file__), "cover.jpg")
    if os.path.exists(image_path):
        pdf.image(image_path, x=10, y=25, w=190)
        pdf.ln(80)  # Move down after image

    # Title
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Executive Summary", ln=True)
    pdf.ln(5)

    # Summary text
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, summary_text)

    pdf.output(output_path)
    print(f"✅ PDF saved to {output_path}")

# Main function to run from app.py
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    # Save text summary
    os.makedirs("ai-market-research", exist_ok=True)
    with open("ai-market-research/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    # Save PDF
    generate_pdf(summary, "ai-market-research/final_report.pdf")
