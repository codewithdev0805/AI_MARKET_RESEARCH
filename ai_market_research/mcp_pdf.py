from flask import Flask, request, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fpdf import FPDF

def generate_pdf(text_file, pdf_file):
    with open(text_file, "r", encoding='utf-8') as f:
        content = f.read()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in content.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(pdf_file)

if __name__ == "__main__":
    generate_pdf("ai-market-research/summary.txt", "ai-market-research/final_report.pdf")
    print("✅ PDF generated.")


app = Flask(__name__)

@app.route("/call-tool", methods=["POST"])
def call_tool():
    data = request.json
    if data["name"] == "generate_pdf":
        insights = data["parameters"]["insights"]
        filename = "report.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        c.drawString(100, 750, "Market Research Report")
        y = 700
        for insight in insights:
            c.drawString(100, y, f"- {insight}")
            y -= 20
        c.save()
        return jsonify({"message": "PDF generated", "file": filename})
    return jsonify({"error": "Unknown tool"}), 400

if __name__ == "__main__":
    app.run(port=5002)
