import streamlit as st
import os
from ai_market_research.mcp_trends import run_mcp_trends
from ai_market_research.analysis_agent import run_analysis_agent
from ai_market_research.report_agent import run_report_agent

st.title("✅ Streamlit App Loaded!")
st.write("If you're seeing this, the app is working.")

st.set_page_config(page_title="Market Research Agent", layout="centered")
st.title(" AI-Powered Market Research Generator")

keyword = st.text_input("Enter a keyword or industry:")

if st.button("Generate Market Report"):
    if not keyword.strip():
        st.warning("Please enter a keyword.")
    else:
        with st.spinner("Running market analysis agents..."):
            run_mcp_trends(keyword)
            run_analysis_agent(keyword)
            run_report_agent()

        st.success(" Report generated!")

        pdf_path = "ai-market-research/final_report.pdf"
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(" Download PDF Report", f, file_name="market_report.pdf")
        else:
            st.error("Report not found. Please check for errors in your script.")
