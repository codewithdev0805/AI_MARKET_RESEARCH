import os
import streamlit as st
from groq import Groq

def run_analysis_agent(keyword):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    raw_trends_path = "ai-market-research/raw_trends.txt"
    with open(raw_trends_path, "r", encoding="utf-8") as f:
        raw_trends = f.read()

    # ✅ Strict keyword filter before sending to LLaMA
    filtered_trends = "\n".join(
        [line for line in raw_trends.split("\n") if keyword.lower() in line.lower()]
    )
    if not filtered_trends.strip():
        filtered_trends = f"No relevant trends found for {keyword}."

    prompt = f"""
    You are a market research analyst.
    ONLY talk about '{keyword}' in the market context.
    Ignore unrelated industries, brands, or events even if they appear in the data.
    
    Here is the research data:
    {filtered_trends}

    Produce a strategy in a structured, clear format.
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    strategy_text = completion.choices[0].message.content

    with open("ai-market-research/strategy.txt", "w", encoding="utf-8") as f:
        f.write(strategy_text)

    print(f"✅ Strategy generated for {keyword}")
