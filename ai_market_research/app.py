import streamlit as st
import os
from mcp_trends import run_mcp_trends
from analysis_agent import run_analysis_agent
from report_agent import run_report_agent

st.set_page_config(page_title="Market Research Agent", layout="centered")

st.title("🧠 AI-Powered Market Research Generator")
st.write("Enter a topic to generate a full market research report.")

keyword = st.text_input("🔍 Enter a keyword or industry:")

if st.button("🚀 Generate Market Report"):
    if not keyword.strip():
        st.warning("⚠️ Please enter a valid keyword.")
    else:
        with st.spinner("🛠 Running market analysis agents..."):
            try:
                run_mcp_trends(keyword)  # Fetch raw trend data
                run_analysis_agent(keyword)  # Write strategy.txt
                run_report_agent()  # Generate summary.txt → final_report.pdf
            except FileNotFoundError as fnf:
                st.error(f"❌ File not found: {fnf}")
            except Exception as e:
                st.error("❌ An unexpected error occurred.")
                st.exception(e)
            else:
                st.success("✅ Report generated successfully!")

        # 🎯 Provide download link
        pdf_path = "ai-market-research/final_report.pdf"
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download PDF Report", f, file_name="market_report.pdf")
        else:
            st.error("❌ PDF report not found. Make sure PDF generation microservice is running.")
