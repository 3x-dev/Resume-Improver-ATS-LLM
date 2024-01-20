import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Act like a skilled or highly experienced ATS (Application Tracking System) 
with a deep understanding of the tech field, software engineering, data science, 
data analysis, big data engineering, and machine learning. Your task is to evaluate resumes 
based on the given job description. Consider that the job market is very 
competitive, and you should provide the best assistance for improving the resumes. 
Assign the percentage match based on the Job Description (JD) and identify the 
missing keywords with high accuracy.

resume:{text}
job description (JD):{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)

        # Print extracted text for verification
        st.subheader("Extracted Text from Your Resume:")
        st.text(text)

        # Continue with processing the text
        response = get_gemini_repsonse(input_prompt)
        st.subheader(response)