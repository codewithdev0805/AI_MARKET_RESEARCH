import os
import requests
from fpdf import FPDF
import streamlit as st
from groq import Groq

# ✅ Load Groq API key
api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key)

# 🧠 Summarize strategy using Groq LLaMA
def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ strategy file not found: {file_path}")

    with open(file_path, "r", encoding='utf-8') as f:
        strategy = f.read()

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a professional market research analyst. Summarize the given strategy into a concise, structured, and visually appealing business report."},
            {"role": "user", "content": strategy}
        ]
    )

    return response.choices[0].message.content.strip()


# 📄 PDF Class with Blue Header & Image
class PDF(FPDF):
    def header(self):
        # Blue rectangle header
        self.set_fill_color(0, 102, 204)
        self.rect(0, 0, 210, 30, 'F')
        
        # Title text
        self.set_text_color(255, 255, 255)
        self.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)  # Only normal font
        self.set_font("DejaVu", "", 18)  # Simulate bold with bigger size
        self.cell(0, 12, "Market Research Report", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_text_color(169, 169, 169)
        self.set_font("DejaVu", "", 10)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


# 📄 Generate PDF
def generate_pdf(summary, output_path):
    pdf = PDF()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)  # Only normal font
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add image
    try:
        img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Market-trends.jpg/640px-Market-trends.jpg"
        img_path = "market_image.jpg"
        r = requests.get(img_url)
        with open(img_path, "wb") as f:
            f.write(r.content)
        pdf.image(img_path, x=10, y=35, w=190)
        pdf.ln(70)
    except Exception as e:
        print(f"⚠️ Could not load image: {e}")

    # Report content
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVu", "", 12)
    pdf.multi_cell(0, 8, summary)

    pdf.output(output_path)
    print(f"✅ PDF saved at {output_path}")


# 🚀 Main Function
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    # Save summary
    output_txt = "ai-market-research/summary.txt"
    os.makedirs(os.path.dirname(output_txt), exist_ok=True)
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(summary)

    # Generate beautiful PDF
    generate_pdf(summary, "ai-market-research/final_report.pdf")


if __name__ == "__main__":
    run_report_agent()
