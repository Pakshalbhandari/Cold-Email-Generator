import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import sys
from chains import Chain
from myskills import Skills
from utils import clean_text
import traceback


def create_streamlit_app(llm, skills, clean_text):
    st.title("Cold E-Mail Generator")
    url_input = st.text_input("Enter a job posting URL")
    submit_button = st.button("Click to Submit")

    if submit_button:
        if not url_input.strip():
            st.warning("Please enter a valid URL.")
            return
        
        try:
            # Load job data
            loader = WebBaseLoader([url_input])
            raw_data = loader.load().pop().page_content
            data = clean_text(raw_data)
            # Load skills and extract jobs
            skills.load_skills()
            jobs = llm.extract_jobs(data)
            if not jobs:
                st.warning("No jobs found in the provided URL.")
                return
            
            # Process each job
            st.write("Skills extracted from jobs")
            st.write(jobs)
            job = jobs[0]
            job_skills = job.get('skills', [])
            # Query portfolio for relevant links
            try:
                links = skills.query_links(job_skills)
            except Exception as e:
                links = []
            
            # Generatz̄e email
            try:
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
            except Exception as e:
                st.error(f"Failed to generate email: {e}")
        
        except Exception as e:
            st.error(f"An Error Occurred: {e} ")



if __name__ == "__main__":
    chain = Chain()
    portfolio = Skills()
    st.set_page_config(layout="wide", page_title="Cold E-Mail Generator")
    create_streamlit_app(chain, portfolio, clean_text)