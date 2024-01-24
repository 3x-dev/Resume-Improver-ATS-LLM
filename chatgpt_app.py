import streamlit as st
import PyPDF2 as pdf
import openai

def get_openai_response(api_key, input_text, job_description):
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Act like a skilled or highly experienced ATS (Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, big data engineering, machine learning, and deep learning. Evaluate resumes concisely and accurately based on the job description (JD). Provide a brief and easy to read summary including the percentage match with the JD, key missing skills or keywords in short bullet points, and a short profile summary in short bullet points. Determine the percentage match with the JD critically based on the missing skills and keywords and user profile matching."
                },
                {
                    "role": "user",
                    "content": f"Resume: {input_text}\nJob Description: {job_description}"
                }
            ],
            max_tokens=200
        )
        return response.choices[0].message['content']
    except openai.error.InvalidRequestError as e:
        return f"Error: {e}"

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Streamlit app
st.title("AI Driven ATS - Resume Improver")
st.text("Improve your resume for tech/machine learning jobs!\nIf JD percentage match is above 85%, consider applying.\nMade by Aryan Singhal - https://www.aisinghal.com/")

# User enters their OpenAI API key
user_api_key = st.text_input("Enter your OpenAI API key")

jd = st.text_area("Paste the Job Description (JD)")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and user_api_key:
        text = input_pdf_text(uploaded_file)
        response = get_openai_response(user_api_key, text, jd)
        st.subheader("Response")
        st.text(response)
    elif not user_api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        st.error("Please upload your resume.")
