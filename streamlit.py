import streamlit as st
import requests
import os


st.title("CV and Job Description Analyzer")

cv_file = st.file_uploader("Upload CV", type=["pdf", "txt"])
jd_file = st.file_uploader("Upload Job Description", type=["pdf", "txt"])

st.sidebar.title("API key")
token = st.sidebar.text_input("Enter your Open AI Key", type="password")
if st.button("Analyze"):
    if cv_file is not None and jd_file is not None and token is not None:
        url = "http://fastapi:8000/upload/"

        files = {
            'cv': (cv_file.name, cv_file, cv_file.type),
            'job_description': (jd_file.name, jd_file, jd_file.type)
        }
        params = {
            'token': token
        }
        try:

            response = requests.post(url, files=files, params=params)

            if response.status_code == 200:
                analysis_result = response.json()
                st.json(analysis_result)
            else:
                st.error(f"Error: {response.status_code}, {response.text}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload both files.")
