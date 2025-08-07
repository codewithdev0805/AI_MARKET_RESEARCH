# main.py
import mcp_trends
import analysis_agent
import report_agent
import mcp_pdf

def run_pipeline(keyword):
    print(f"🚀 Running AI Market Research for: {keyword}")
    mcp_trends.fetch_market_trends(keyword)
    analysis_agent.run_analysis()
    report_agent.run_summary()
    mcp_pdf.generate_pdf("ai-market-research/summary.txt", "ai-market-research/final_report.pdf")
    print("✅ All Done! PDF Ready.")

if __name__ == "__main__":
    kw = input("Enter keyword: ")
    run_pipeline(kw)
