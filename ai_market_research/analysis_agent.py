import os
import streamlit as st
from groq import Groq

# Load API key and model from secrets (or env fallback)
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
model_name = st.secrets.get("GROQ_MODEL", "llama-3.3-70b-versatile")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in Streamlit secrets or environment variables.")

client = Groq(api_key=api_key)

def run_analysis_agent(keyword):
    prompt = f"""
    You are a market research analyst.
    Generate a detailed market analysis for the keyword: '{keyword}'.
    Provide insights, opportunities, risks, and recent trends.
    """

    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )

    strategy_text = completion.choices[0].message.content.strip()

    # Save to strategy.txt
    os.makedirs("ai-market-research", exist_ok=True)
    with open("ai-market-research/strategy.txt", "w", encoding="utf-8") as f:
        f.write(strategy_text)

    print("✅ Strategy saved to ai-market-research/strategy.txt")
