import resumescoringsystem as rs
import streamlit as st
import pandas as pd


def get_info():
    st.title('Behind the Scenes')
    st.caption('This page explains the code behind the webapp')

    st.header('1. Importing the necessary libraries')
    st.write('First I am going to import all the required libraries. The libraries used in this project are pandas, streamlit and resumescoringsystem. The resumescoringsystem is a custom library that I have created to rate the resumes based on the job description. The pandas library is used to create the dataframe and streamlit is used to create the webapp.')

    st.header('2. Loading the files')
    st.write('The load_file function is used to load the resume files and the load_job_description function is used to load the job description file. The load_file function reads the binary data from the database and converts it into a file-like object. The file-like object is then used to read the PDF file and extract the text content. The load_job_description function does the same thing but for the job description file.')

    st.header('3. Rating the resumes')
    st.write('The rate_resume function is used to rate the resumes based on the job description. The function takes the text content of the resume and the job description as input and returns the response. The response is a dictionary that contains the keywords from the job description and the count of those keywords in the resume.')

    st.header('4. Extracting notes for each resumes')
    st.write('The extract_note function is used to extract the notes for each resume. The function takes the response as input and returns the notes. The notes are extracted based on the keywords from the job description and the count of those keywords in the resume.')

    st.header('5. Getting the scores')
    st.write('The find_score function is used to find the score for each resume. The function takes the response as input and returns the score. The score is calculated based on the count of the keywords from the job description in the resume.')

    st.header('6. Finalizing the result')
    st.write('The save_result function is used to save the result in a CSV file. The function takes the dataframe as input and saves it in a CSV file. The dataframe contains the resume name, score, note and response for each resume. The dataframe is then sorted based on the score in descending order.')

    st.header('7. Creating the dataframe')
    st.write('The process function is used to create the dataframe. The function takes the resume files and the job description file as input and returns the notes for each resume. The function first loads the files and the job description. It then rates the resumes, extracts the notes and gets the scores. Finally, it creates the dataframe and sorts it based on the score in descending order.')

    st.header('8. Setting the page configuration')
    st.write('The set_page_config function is used to set the page configuration. The function takes the page title, page icon, layout and initial sidebar state as input. The page title is set to "Resume Scoring System", the page icon is set to "human-resources.png", the layout is set to "centered" and the initial sidebar state is set to "auto".')

    st.header('9. Displaying the result')
    st.write('The title, caption and dataframe are displayed on the webapp. The title is set to "Resume Scoring System" and the caption is set to "This webapp is used to rate the resumes based on the job description". The dataframe contains the resume name and the score for each resume. The dataframe is then displayed on the webapp.')

    st.header('10. Conclusion')
    st.write('In this project, I have created a webapp that rates the resumes based on the job description. The webapp uses the resumescoringsystem library to rate the resumes. The library contains functions to load the files, rate the resumes, extract the notes, get the scores and save the result. The webapp also uses the pandas library to create the dataframe and the streamlit library to create the webapp. The webapp displays the title, caption and the dataframe on the webapp. The title is set to "Resume Scoring System" and the caption is set to "This webapp is used to rate the resumes based on the job description". The dataframe contains the resume name and the score for each resume. The dataframe is then displayed on the webapp.')

    st.header('11. References')
    st.write('1. https://pandas.pydata.org/docs/')
    st.write('2. https://www.streamlit.io/')
    st.write('3. https://www.openai.com/')

# Function to display messages
def display_message(message):
    placeholder = st.empty()  # Create an empty placeholder
    placeholder.write(message)
    

def process(files,uploaded_job_file):
    df = pd.DataFrame()
    text_data = []
    responses = []
    notes = []
    scores = []
    with st.spinner("Loading the files..."):
        for file in files:
           # print(file.name)
            text_data.append(rs.load_file(file.name))
        job_description = rs.load_job_description(uploaded_job_file.name)
        #print(len(text_data))
    #print(job_description)

    with st.spinner("Rating the resumes..."):
        progress = st.progress(0)
        for (i,text) in enumerate(text_data):
            response = rs.rate_resume(text, job_description)
            msg = f'{i+1} files rated successfully'
            print(msg)
            progress.progress((i+1)/len(text_data))
            responses.append(response)
        # now remove the bar
        progress.empty()
        #st.success('Resumes rated successfully')
        
    with st.spinner("Extracting notes for each resumes..."):
        
        for (i,response) in enumerate(responses):
            note = rs.extract_note(response)
            print(f'{i+1} files extracted successfully')
            notes.append(note)
        #print(notes[-1])
    #st.success('Notes extracted successfully')
          
    with st.spinner("Getting the scores..."):
        progress = st.progress(0)
        for (i,response) in enumerate(responses):
            score = rs.find_score(response)
            msg = f'{i+1} files scored successfully'
            print(msg)
            progress.progress((i+1)/len(responses))
            scores.append(float(score))
        print(scores)
        progress.empty() 
    #st.success('Scores extracted successfully')
                
    with st.spinner("Finalizing the result..."):
        df = pd.DataFrame({'Resume': [file.name for file in files], 'Score': scores, 'Note': notes, 'Response': responses})
        df.sort_values(by='Score', ascending=False, inplace=True)
    
    
    #st.success('Dataframe created successfully')       
    st.write(df[['Resume','Score']])
    #st.write(responses[0])

    return df
    
# Set the page configuration
st.set_page_config(page_title='Resume Scoring System', page_icon='logo.png' , layout='centered', initial_sidebar_state='auto')
st.title('Resume Scoring System')

st.caption('This webapp is used to rate the resumes based on the job description')


# want to know the what is happening behind
st.sidebar.header('Behind the Scene')
st.sidebar.caption('Want to know what is happening behind the scene?')

if st.sidebar.button('Yes, I want to know'):
    get_info()
st.sidebar.divider()

# Set the sidebar title
st.sidebar.header('Upload Files')

# Set the sidebar description
st.sidebar.caption('Upload the job description and resumes to rate the resumes')

# Upload the job description file
uploaded_job_file = st.sidebar.file_uploader('Upload the job description file', type=['pdf'])

# Upload the resume files
uploaded_file = st.sidebar.file_uploader('Upload the resume files', type=['pdf'], accept_multiple_files=True)
st.sidebar.caption('As this is a demo version, you can upload only 4 resumes')
files = []

job_description = ''
# Generate the scores

if st.sidebar.button('Generate Scores'):
    if not uploaded_file or not uploaded_job_file:
        st.warning("There is some error while uploading the files or may be you didn't upload the files. Please upload the files and try again.")
    else:
        st.caption('It may take some time to process the files. Please wait...')
        rs.save_job_description(uploaded_job_file.name,uploaded_job_file)
        if len(uploaded_file) > 4:
            st.warning('You have uploaded more than 4 files.Please upload only 5 files.')
        else:
            for (i,file) in enumerate(uploaded_file):
                rs.save_file(file.name,file)
                print(f"data/{file.name}")
                
            #print("Processing the files...")
            #st.write("Processing the files...")
            try:
                df = process(uploaded_file,uploaded_job_file)
                print(len(df['Note']))
            except Exception as e:
                st.error(f'An error occurred: {e}')
                print(Exception)
            else:
                print(df.shape)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name="result.csv",
                    mime="text/csv",
                )
                flag = 1
                st.write('The resumes are rated successfully. Please check the notes below')
                for i,note in enumerate(df['Note']):
                    st.write(f'Resume {i+1}')
                    st.markdown(note)

with st.sidebar:
    st.header("👩‍💻 **About the Creator**")
    st.write("I am a Data Science enthusiast with a passion for solving real-world problems using data. I have experience in building machine learning models, data analysis, and data visualization. I am always eager to learn new technologies and explore new domains. I am currently looking for opportunities in Data Science and Machine Learning.")
    st.write("Let's connect to explore opportunities, share knowledge, and collaborate on exciting projects!") 
    st.write("🔗 **Connect with Me:**")
    #st.write("[🌐 Portfolio](https://www.google.com/)") 
    st.write("[📧 Email](mailto:kirtipogra@gmail.com)")
    st.write("[📝 LinkedIn](https://www.linkedin.com/in/kirti-pogra/)")

