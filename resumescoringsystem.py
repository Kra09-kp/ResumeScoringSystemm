from pypdf import PdfReader
import openai
from openai import OpenAI
import sqlite3
import io

# Function to read the api keys
def read_api_key(file_path):
    with open(file_path, 'r') as file:
        api_key = file.readline()
    return api_key
openai.api_key = read_api_key("openai_api_key.txt")

client = OpenAI(api_key = openai.api_key)

system  = "You are a HR bot.You will be provided a resume and job description.You need to calculate total score based on given criteria without taking any assumptions.\
    Remember, Stricktly follow that total score are less that or equal to 10."

assistant = "Hello! As the HR bot, your task is to assess a resume in comparison to a given job description. Here's what you need to do:\n\n\
            You'll analyze the resume in relation to the provided job description: {doc}. Your evaluation will be based on the following criteria:\n\n\
                -Assign a scores out of 5 if the candidate meets all the minimum qualifications.(For this section total score must not be greater than five.)\n\
                -Assign a scores out of 3 if the candidate meets all the preferred qualifications.(For this section total score must not be greater than Three.)\n\
                -Assign a scores out of 2 if the candidate's previous experience or projects align with the job responsibilities.(For this section total score must not be greater than Two.)\n\n\
            Finally, calculate the total score out of 10 and In last give the total score . Remember, the total score must not exceed 10.\n\n\
            Additionally, you can offer suggestions to the HR team in the Note section. This could include a quick summary of the resume and any standout strengths or areas for improvement."

def rate_resume(doc,text):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        temperature = 0, #high temperature mean more randomness, which we don't want in our result
        top_p=0.05,
        seed = 123,
        messages = [
            {
                "role": "system",
                "content" : system
            },
            {
                "role": "assistant",
                "content":assistant.format(doc = doc)},
            {
                "role":"user",
                "content": f"Here is the provided resume: {text}. Examine this and give the total score based on the given criteria.Remember, the total score must not exceed 10."
            }
        ]
    )
    return response.choices[0].message.content

def find_score(text):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        temperature = 0, #high temperature mean more randomness, which we don't want in our result
        top_p=1,
        messages = [
            {
                "role": "assistant",
                "content":"Extract what is the total score in the text and provide it without any explanation and other stuff. Give the total score as a number(0 to 10).\
                    If the total score is greater than 10, then give your total score which you think it should be based on the given criteria.\n\n\
                        Remember, the total score must not exceed 10.\n\n\
                        Here is the given criteria:\n\n\
                            -Assign a scores out of 5 if the candidate meets all the minimum qualifications.(For this section total score must not be greater than five.)\n\
                            -Assign a scores out of 3 if the candidate meets all the preferred qualifications.(For this section total score must not be greater than Three.)\n\
                            -Assign a scores out of 2 if the candidate's previous experience or projects align with the job responsibilities.(For this section total score must not be greater than Two.)\n\n\
                        Finally, calculate the total score out of 10 and In last give the total score . Remember, the total score must not exceed 10."},
            {
                "role":"user",
                "content": f"Here is given text {text}. Give what is the total score present in the Total Score section of the text. "
            }
        ]
    )
    return response.choices[0].message.content

# Find the start of the "Note" section
def extract_note(response_text):
    start_index = response_text.find("Note:")

    # Extract the "Note" section
    note_section = response_text[start_index:]

    # Print the extracted "Note" section
    note = note_section.strip()
    #display(Markdown(note))
    return note


def save_file(file_name,file):
    
    pdf_binary_data = file.read()
        

    # Connect to SQLite database
    conn = sqlite3.connect('ResumeData.db')

    # Insert PDF data into the database
    cursor = conn.cursor()

    # Create a table to store PDF files
    cursor.execute("CREATE TABLE IF NOT EXISTS resume_files (file_name TEXT, file_data BLOB)")
    cursor.execute("INSERT INTO resume_files (file_name, file_data) VALUES (?, ?)",
               (file_name, pdf_binary_data))
    conn.commit()

    conn.close()

def save_job_description(file_name,file):
    pdf_binary_data = file.read()

    # Connect to SQLite database
    conn = sqlite3.connect('ResumeData.db')

    # Insert PDF data into the database
    cursor = conn.cursor()

    # Create a table to store PDF files
    cursor.execute("CREATE TABLE IF NOT EXISTS job_description (file_name TEXT, file_data BLOB)")
    cursor.execute("INSERT INTO job_description (file_name, file_data) VALUES (?, ?)",
               (file_name, pdf_binary_data))
    conn.commit()

    conn.close()


def load_file(file_name):
    # Connect to SQLite database
    conn = sqlite3.connect('ResumeData.db')
    cursor = conn.cursor()

    # Retrieve PDF data from the database
    cursor.execute("SELECT file_data FROM resume_files WHERE file_name = ?", (file_name,))
    pdf_binary_data = cursor.fetchone()[0]
    # Close the database connection
    conn.close()

    # Convert binary data into a file-like object
    file_like_object = io.BytesIO(pdf_binary_data)

    # Read the PDF file and extract text content
    text = ""
    reader = PdfReader(file_like_object)
    for page in reader.pages:
        text += page.extract_text()

    return text

def load_job_description(file_name):
    # Connect to SQLite database
    conn = sqlite3.connect('ResumeData.db')
    cursor = conn.cursor()

    # Retrieve PDF data from the database
    cursor.execute("SELECT file_data FROM job_description WHERE file_name = ?", (file_name,))
    pdf_binary_data = cursor.fetchone()[0]

    # Close the database connection
    conn.close()

    # Convert binary data into a file-like object
    file_like_object = io.BytesIO(pdf_binary_data)

    # Read the PDF file and extract text content
    text = ""
    reader = PdfReader(file_like_object)
    for page in reader.pages:
        text += page.extract_text()

    return text


def save_result(df):
    '''
    df is the dataframe which have three column resume name, scores,notes and response'''

    # Connect to SQLite database
    conn = sqlite3.connect('ResumeData.db')

    # Insert dataframe into the database
    cursor = conn.cursor()

    # Create a table to store dataframe
    cursor.execute("CREATE TABLE IF NOT EXISTS resume_result (resume_name TEXT, scores TEXT, notes TEXT, response TEXT)")
    for i in range(len(df)):
        cursor.execute("INSERT INTO resume_result (resume_name, scores, notes, response) VALUES (?, ?, ?, ?)",
               (df['Resume'][i], df['Score'][i], df['Note'][i], df['Response'][i]))
            
    conn.commit()

    conn.close()
