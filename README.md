# Resume Scoring System

## Table of Contents
1. [Introduction](#Introduction)
2. [How to use the system](#How-to-use-the-system)
3. [How to run the system locally](#How-to-run-the-system-locally)
4. [File included](#File-included)
5. [Libraries used](#Libraries-used)
6. [Conclusion](#Conclusion)


## Introduction
This project is a resume-scoring system based on the job description. The system uses a pre-trained Openai model named chat-GPT to score resumes. The system is built using the Streamlit library in Python. The system is deployed on the Strealit sharing platform.

## How to use the system

1. Open the system using the following link: [Resume Scoring System](https://resumescoringsystem.streamlit.app/)
2. Upload the pdf file of the job description.
3. Upload the pdf file of the resumes.
4. Click on the "Generate Score" button to get the scores of the resumes.
5. You can download the result in CSV file format by clicking the "Download Result" button.

## How to run the system locally

1. Clone the repository using the following command:
```bash
git clone
```
2. Install the required libraries using the following command:
```bash
pip install -r requirements.txt
```
3. Run the following command to run the system:
```bash
streamlit run app.py
```

## File included 
1. app.py: This file contains the code for the resume scoring system.
2. requirements.txt: This file contains the required libraries to run the system.
3. README.MD: This file contains information about the project.
4. resumescoringsystem.py: This file contains the functions that I use in the app.py file.
5. genai_api_key.txt: This file contains genai api key. This file is not included in the repo you need to create that one for yourself.

   
## Libraries used
1. Streamlit
2. PyPDF2
3. genai
4. Pandas

## Conclusion
The resume scoring system is useful for HR professionals to score resumes based on the job description. The system uses a pre-trained Openai model to score resumes. The system is built using the Streamlit library in Python. The system is deployed on the Streamlit sharing platform.









