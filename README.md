# Cold E-Mail Generator

A web application that generates personalized and professional cold emails for job applications using AI. The app takes a job posting URL as input, extracts job descriptions, and crafts tailored emails highlighting technical skills, professional experience, and impactful projects.

## Features
- Extracts job postings from provided URLs.
- Cleans and processes text for job extraction.
- Matches relevant skills and links from a portfolio.
- Generates personalized emails for job applications.

## Tech Stack
- **Streamlit**: For creating an interactive web application.
- **LangChain**: For chaining AI models and prompt engineering.
- **Python**: Backend logic and text processing.
- **dotenv**: For secure management of API keys and environment variables.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Pakshalbhandari/Cold-Email-Generator.git
cd cold-email-generator
```


## Usage
### 1. Run the Streamlit App
streamlit run app/main.py

### 2. Interact with the App
- Enter a job posting URL in the input field.
- Click "Click to Submit" to generate a personalized email.

