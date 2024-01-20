import streamlit as st
import os
import PyPDF2 as pdf
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI with your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(input_text, job_description):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Act like a skilled or highly experienced ATS (Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, big data engineering, machine learning, and deep learning. Evaluate resumes concisely and accurately based on the job description (JD). Provide a brief and easy to read summary including the percentage match with the JD, key missing skills or keywords in short bullet points, and a short profile summary in short bullet points."
            },
            {
                "role": "user",
                "content": f"Resume: {input_text}\nJob Description: {job_description}"
            }
        ],
        max_tokens=300 #change to reduce output
    )
    return response.choices[0].message['content']

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_openai_response(text, jd)
        st.subheader("Response")
        st.text(response)