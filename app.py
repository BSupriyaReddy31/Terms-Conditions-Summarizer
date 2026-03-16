import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- CONFIGURATION ---
genai.configure(api_key="YOUR_GEMINI_API_KEY")
st.set_page_config(page_title="T&C AI Summarizer", page_icon="⚖️")

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_tc(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are a specialized legal AI. Analyze the following Terms and Conditions text. 
    Focus on consumer rights, data privacy, and potential "gotchas."
    
    Provide the analysis in this structure:
    - **Executive Summary**: 2 sentences max.
    - **Risk Score**: A score from 1 (Safe) to 10 (Dangerous).
    - **The Red Flags**: List specific clauses that are anti-consumer (e.g., forced arbitration, data selling).
    - **Data Privacy**: How is the data handled?
    - **Cancellation**: How easy is it to leave?
    
    Text to analyze:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text

# --- UI DESIGN ---
st.title("⚖️ AI Terms & Conditions Summarizer")
st.markdown("Upload a PDF or paste the text to find out what you're actually signing.")

tab1, tab2 = st.tabs(["Upload PDF", "Paste Text"])

with tab1:
    uploaded_file = st.file_uploader("Choose a T&C PDF file", type="pdf")
    if uploaded_file and st.button("Analyze PDF"):
        with st.spinner("Reading and analyzing..."):
            raw_text = extract_text_from_pdf(uploaded_file)
            analysis = analyze_tc(raw_text)
            st.markdown(analysis)

with tab2:
    user_text = st.text_area("Paste T&C text here...", height=300)
    if user_text and st.button("Analyze Text"):
        with st.spinner("Analyzing legal jargon..."):
            analysis = analyze_tc(user_text)
            st.markdown(analysis)

st.divider()
st.caption("Disclaimer: This tool provides AI-generated summaries and does not constitute legal advice.")
