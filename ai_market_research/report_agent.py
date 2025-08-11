import os
import streamlit as st
from fpdf import FPDF
from groq import Groq

# ✅ Load API key and model name from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]
model_name = st.secrets.get("MODEL_NAME", "llama-3.3-70b-versatile")

# Initialize Groq client
client = Groq(api_key=api_key)

# 📌 Summarize strategy file
def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        strategy = f.read()

    prompt = f"You are a market research analyst. Summarize this in a well-structured, professional business report format:\n\n{strategy}"

    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


# 📄 PDF Template Class
class PDF(FPDF):
    def header(self):
        # Blue header background
        self.set_fill_color(0, 102, 204)
        self.rect(0, 0, 210, 40, "F")

        # Document Icon
        icon_path = "ai-market-research/assets/document_icon.png"
        if os.path.exists(icon_path):
            self.image(icon_path, x=85, y=5, w=40)

        # Move below image and set title
        self.set_xy(10, 30)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "Market Research Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_body(self, text):
        self.set_text_color(0)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, text)
        self.ln()


# 📌 Generate PDF
def generate_pdf(summary, output_path):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.chapter_body(summary)
    pdf.output(output_path)
    print(f"✅ PDF saved at {output_path}")


# 🚀 Main Function
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    # Save summary.txt
    with open("ai-market-research/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    # Generate PDF
    generate_pdf(summary, "ai-market-research/final_report.pdf")
    print("✅ Final report PDF generated!")


if __name__ == "__main__":
    run_report_agent()
