import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0.5, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile",max_retries=2,)

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
            res = res[0]
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]
    
    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}
        
        ### INSTRUCTION:
        You are Pakshal, a masters in computer science students at Purdue University.
        I want to write a professional cold email introducing myself to [specific person or organization] and keep it realted according to job description. 
        The email should highlight my technical expertise and professional experience, including 3 years as a Software Engineer specializing in backend development with Python, SQL, and Django, where I optimized system performance and enhanced security. 
        Mention my role as a Teaching Assistant at Purdue University, where I automated grading using Python and engineered an LLM-based grading system. 
        Additionally, include my internship at Quicken, where I integrated customer data across databases, built insightful dashboards, and resolved critical bugs in SQL pipelines. 
        Highlight my impactful projects, such as developing a Python-based question speech bot with 99% uptime, creating a gender bias detection framework for LLMs, and achieving 95.8 accuracy in fake news detection. 
        The tone should be professional and engaging, with a clear call to action to discuss how my skills align with [specific goals or projects]. 
        Also add the most relevant ones from the following links to showcase experience: {link_list}
        Remember you are Pakshal, grad student at Purdue University. 
        Do not provide a preamble and keep proper spacing and alignment.
        ### EMAIL (NO PREAMBLE):
        
        """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content
    

if __name__ == "__main__":

    if os.getenv("GROQ_API_KEY") is None:
        raise Exception("Please set the environment variable GROQ_API_KEY") 