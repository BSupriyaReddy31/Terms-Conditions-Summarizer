import streamlit as st
from google import genai
from PyPDF2 import PdfReader
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="T&C AI Summarizer", page_icon="⚖️", layout="wide")

# --- SECURE API KEY LOADING ---
# If running locally, it looks for an environment variable. 
# If on Streamlit Cloud, it looks in "Secrets".
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key not found! Please add GEMINI_API_KEY to Streamlit Secrets or Environment Variables.")
    st.stop()

client = genai.Client(api_key=api_key)

# --- HELPER FUNCTIONS ---
def extract_text_from_pdf(file):
    try:
        pdf_reader = PdfReader(file)
        text = "".join([page.extract_text() for page in pdf_reader.pages])
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def analyze_tc(text):
    prompt = f"""
    Analyze the following Terms and Conditions text as a consumer rights advocate.
    Provide a clear, structured report:
    1. **Summary**: What is this service?
    2. **Risk Score (1-10)**: How dangerous is this for the user?
    3. **Key Red Flags**: List specific clauses like data selling, forced arbitration, or hidden fees.
    4. **Privacy & Data**: Who gets the user's data?
    5. **Verdict**: Final recommendation (e.g., Safe, Proceed with Caution, Avoid).

    Text:
    {text}
    """
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI Analysis failed: {e}"

# --- USER INTERFACE ---
st.title("⚖️ Professional T&C Summarizer")
st.info("Upload a legal document to uncover hidden risks using Gemini 1.5 Flash.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Document")
    source_option = st.radio("Choose Input Type:", ["Upload PDF", "Paste Text"])
    
    input_text = ""
    
    if source_option == "Upload PDF":
        uploaded_file = st.file_uploader("Upload T&C PDF", type="pdf")
        if uploaded_file:
            input_text = extract_text_from_pdf(uploaded_file)
    else:
        input_text = st.text_area("Paste the legal text here...", height=300)

    analyze_btn = st.button("🔍 Run Risk Analysis", use_container_width=True)

with col2:
    st.subheader("Analysis Results")
    if analyze_btn and input_text:
        with st.spinner("Gemini is reading the fine print..."):
            result = analyze_tc(input_text)
            st.markdown(result)
    elif analyze_btn and not input_text:
        st.warning("Please provide some text or a PDF first!")

st.divider()
st.caption("Built for B.Tech Final Year Project - Powered by Gemini 1.5")
