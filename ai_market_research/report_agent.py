import os
import requests
from flask import Flask, request, jsonify
from fpdf import FPDF
from groq import Groq  # ✅ LLaMA client

# ====== Load API key ======
try:
    import streamlit as st
    API_KEY = st.secrets.get("GROQ_API_KEY", None)
except:
    API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in Streamlit secrets or environment variables.")

# ✅ Initialize Groq client
client = Groq(api_key=API_KEY)


# ====== AI CALL ======
def call_ai_model(prompt: str) -> str:
    """Send prompt to LLaMA via Groq and return response text."""
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # You can use llama3-70b-8192 if needed
        messages=[
            {"role": "system", "content": "You are a market research analyst. Respond in structured bullet points."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    return response.choices[0].message.content.strip()


# ====== PDF GENERATOR ======
def generate_pdf(data, output_path):
    """Generate a clean, professional PDF report."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, data["title"])
    pdf.ln(5)

    # Key Highlights
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Key Highlights:", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for item in data["key_highlights"]:
        pdf.multi_cell(0, 8, f"• {item}")
    pdf.ln(3)

    # Business Implications
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Business Implications:", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for item in data["business_implications"]:
        pdf.multi_cell(0, 8, f"• {item}")
    pdf.ln(3)

    # Recommendations
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Recommendations:", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for item in data["recommendations"]:
        pdf.multi_cell(0, 8, f"• {item}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"✅ PDF saved to {output_path}")


# ====== MAIN FUNCTION ======
def run_report_agent():
    strategy_path = "ai-market-research/strategy.txt"
    if not os.path.exists(strategy_path):
        raise FileNotFoundError("❌ strategy.txt not found. Run analysis_agent first.")

    with open(strategy_path, "r", encoding="utf-8") as f:
        strategy = f.read()

    # Ask AI to structure content
    prompt = f"""
    Summarize the following strategy for a business report.
    Return the result in this structure:
    Title: ...
    Key Highlights: [point1, point2, ...]
    Business Implications: [point1, point2, ...]
    Recommendations: [point1, point2, ...]

    Strategy content:
    {strategy}
    """
    ai_response = call_ai_model(prompt)

    # Parse into structured data
    structured_data = {"title": "", "key_highlights": [], "business_implications": [], "recommendations": []}
    section = None
    for line in ai_response.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("title:"):
            structured_data["title"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("key highlights"):
            section = "key_highlights"
        elif line.lower().startswith("business implications"):
            section = "business_implications"
        elif line.lower().startswith("recommendations"):
            section = "recommendations"
        elif line.startswith("*") or line.startswith("-"):
            if section:
                structured_data[section].append(line[1:].strip())

    # Save summary.txt
    with open("ai-market-research/summary.txt", "w", encoding="utf-8") as f:
        f.write(ai_response)

    # Generate PDF
    generate_pdf(structured_data, "ai-market-research/final_report.pdf")


# ====== FLASK ENDPOINT (optional) ======
app = Flask(__name__)

@app.route("/report", methods=["POST"])
def generate_report():
    insights = request.json.get("insights", "")
    run_report_agent()
    return jsonify({"status": "PDF generated"})


if __name__ == "__main__":
    run_report_agent()
