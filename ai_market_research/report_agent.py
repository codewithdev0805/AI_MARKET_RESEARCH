import os
import requests
from flask import Flask, request, jsonify
from fpdf import FPDF
from llamaapi import LlamaAPI

# 🔹 Initialize LLaMA API
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
if not LLAMA_API_KEY:
    raise ValueError("❌ LLAMA_API_KEY not found in environment variables.")

llama = LlamaAPI(LLAMA_API_KEY)

# 🧠 Summarize strategy using LLaMA
def summarize_strategy(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Strategy file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        strategy = f.read()

    prompt = f"You are a professional market research analyst. Summarize the following strategy into a short, structured, and beautiful report:\n\n{strategy}"

    response = llama.run({
        "model": "llama-3-70b-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    })

    return response.json()["choices"][0]["message"]["content"].strip()

# 🎨 Custom PDF Class for styling
class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 18)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, "📊 AI-Powered Market Research Report", ln=True, align="C")
        self.ln(5)
        self.set_draw_color(0, 102, 204)
        self.set_line_width(1)
        self.line(10, 25, 200, 25)
        self.ln(5)

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

# 📄 Generate PDF
def generate_pdf(summary_text, output_path):
    pdf = PDF()
    try:
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.add_font("DejaVu", "B", "DejaVuSans.ttf", uni=True)
    except:
        print("⚠️ Font not found. Using default Helvetica.")
        pdf.set_font("Helvetica", "", 12)

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.chapter_title("Executive Summary")
    pdf.chapter_body(summary_text)

    pdf.output(output_path)
    print(f"✅ PDF report generated: {output_path}")

# 🚀 Main function for pipeline
def run_report_agent():
    summary = summarize_strategy("ai-market-research/strategy.txt")

    # Save summary text
    summary_path = "ai-market-research/summary.txt"
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print("✅ Summary saved to summary.txt")

    # Generate polished PDF
    generate_pdf(summary, "ai-market-research/final_report.pdf")

# 🌐 Flask API for PDF generation (optional)
app = Flask(__name__)

@app.route("/report", methods=["POST"])
def generate_report():
    insights = request.json.get("insights", "")
    generate_pdf(insights, "ai-market-research/final_report.pdf")
    return jsonify({"status": "success", "message": "PDF generated."})

if __name__ == "__main__":
    run_report_agent()
