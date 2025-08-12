📊 AI Market Research Pipeline (A2A)

An AI-powered Automated-to-Automated (A2A) market research system that fetches real-time trends, analyzes them, and generates professional, visually appealing PDF reports — all without manual intervention.  

This project is inspired by Google A2A concepts and leverages multi-agent orchestration to streamline market research.

---

🚀 Workflow Overview

A2A Flow:
1. Trend Agent → Identifies trending keywords & topics.  
2. Analysis Agent → Performs deep market analysis and prepares `strategy.txt`.  
3. Report Agent → Generates a **beautiful PDF report** with charts, sections, and icons.  

---

✨ Features
- Automated Trend Discovery — fetches market trends dynamically.
- AI-Driven Analysis — powered by Groq’s `llama-3.3-70b-versatile` model.
- Beautiful PDF Reports — includes colors, sections, and optional charts.
- Easy Model Switching — change model from `st.secrets` without touching the code.
- Streamlit Deployment — run on local or cloud.

---

🛠️ Tech Stack
- Languages: Python
- Frameworks: Streamlit, Flask
- AI Models: Groq LLaMA 3.3 70B Versatile
- Libraries: Pandas, Matplotlib, FPDF2
- APIs: Groq API
- Concept: Google A2A (Automated-to-Automated)

---

📂 Project Structure

ai_market_research/
│-- app.py # Streamlit entry point
│-- analysis_agent.py # Gathers & analyzes data
│-- report_agent.py # Generates PDF report
│-- requirements.txt # Dependencies
│-- README.md # Project documentation


💡 This project showcases how multi-agent AI pipelines can automate end-to-end market research, transforming raw trend data into actionable, presentation-ready business reports.
