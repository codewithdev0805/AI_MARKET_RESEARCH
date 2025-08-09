import os
import json
import requests
from fpdf import FPDF
from groq import Groq

# Initialize Groq client (LLaMA 3 via Groq API)
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in environment variables.")
client = Groq(api_key=api_key)

# ──────────────────────────────────────────────
# Call LLaMA Model and Enforce JSON Output
# ──────────────────────────────────────────────
def call_ai_model(prompt: str) -> dict:
    """Send prompt to LLaMA via Groq and return parsed JSON."""
    json_format_instructions = """
    Return ONLY a valid JSON object in this exact format:
    {
      "title": "string",
      "key_highlights": ["point 1", "point 2", "point 3"],
      "business_implications": ["point 1", "point 2"],
      "recommendations": ["point 1", "point 2"]
    }
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a market research analyst. Respond in JSON format only."},
            {"role": "user", "content": prompt + "\n\n" + json_format_instructions}
        ],
        temperature=0.3,
        max_tokens=1500
    )
    raw_output = response.choices[0].message.content.strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        raise ValueError(f"❌ Model did not return valid JSON. Output:\n{raw_output}")

# ──────────────────────────────────────────────
# PDF Generator
# ──────────────────────────────────────────────
def generate_pdf(data: dict, output_path: str):
    """Generate a nicely formatted PDF from structured data."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.multi_cell(0, 10, data.get("title", "Market Research Report"), align="C")
    pdf.ln(5)

    def add_section(title, items):
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Arial", '', 12)
        if items:
            for item in items:
                pdf.multi_cell(0, 8, f"• {item}")
        else:
            pdf.multi_cell(0, 8, "No data available.")
        pdf.ln(3)

    add_section("Key Highlights:", data.get("key_highlights", []))
    add_section("Business Implications:", data.get("business_implications", []))
    add_section("Recommendations:", data.get("recommendations", []))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"✅ PDF saved to {output_path}")

# ──────────────────────────────────────────────
# Main Function
# ──────────────────────────────────────────────
def run_report_agent():
    strategy_path = "ai-market-research/strategy.txt"
    if not os.path.exists(strategy_path):
        raise FileNotFoundError("❌ strategy.txt not found. Run analysis_agent first.")

    with open(strategy_path, "r", encoding="utf-8") as f:
        strategy = f.read()

    prompt = f"Summarize the following strategy for a business report:\n\n{strategy}"
    structured_data = call_ai_model(prompt)

    # Save JSON summary
    with open("ai-market-research/summary.txt", "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=2)

    # Generate PDF
    generate_pdf(structured_data, "ai-market-research/final_report.pdf")
