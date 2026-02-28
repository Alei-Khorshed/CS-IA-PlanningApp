# Import libraries required for this page
import streamlit as st    # main streamlit library 
import pandas as pd       # pandas library for working and displaying with data 
import sqlite3 as sql     # sqllite3 library to work with a sqllite database



# Display the page title at the top of the page and in the left navigation sidebar
st.markdown("# Task Data")
st.sidebar.markdown("# Task Data")

if "first_load" not in st.session_state:
    st.session_state.first_load = "YES"

# Set the variable name for my DB
MyDB = "CS IA DB.db"

# Create DB Connection 
conn = sql.connect(MyDB)



# Read the entire table into a DataFrame
# Create a SQL command to read data from the table 
df = pd.read_sql("SELECT task_id , title , deadline , difficulty , status , date_completed FROM Task", conn)
# Display the dataframe on the page
st.write(df)

# Read subjects to add them to the drop down list of subjects
df_subject = pd.read_sql("SELECT subject_id, title FROM Subject", conn)
subject_titles = df_subject['title'].tolist()


# Create a form to enter data
with st.form("data_form", clear_on_submit=True):
    subject = st.selectbox("Subject Name:", options = subject_titles)    

    title = st.text_input("Task Title", key="txtTitle")
    deadline = st.date_input("Deadline", value="today",format=st.session_state.gDateFormat,key="txtDeadline")


    diff_list = ["Easy", "Medium", "Hard"]
    difficulty = st.selectbox("Difficulty Level:", diff_list)

    # Add a sumbit button
    submit = st.form_submit_button("Add Task")

    # Save the new record into the database
    if submit:
        selected_subject_id = int(df_subject.loc[df_subject['title'] == subject, 'subject_id'].iloc[0])
        #st.write(selected_subject_id)    
        #st.write(subject)
        #st.write(title)

        # Create a DataFrame for the new record
        data_record = [{"task_id":0,   "subject_id": selected_subject_id, "user_id": st.session_state.gCurrentUser, "title":title, "deadline":deadline, "difficulty":difficulty, "status":"PENDING", "date_completed":""}]
        df_data = pd.DataFrame(data_record)
        
        # Create a SQL command to save the record to the database
        cur = conn.cursor()
        cur.executemany("INSERT INTO Task VALUES(NULL,:subject_id, :user_id, :title, :deadline, :difficulty, :status, :date_completed)", data_record)
        # Commit Database to save changes
        conn.commit() 

        st.session_state.first_load = "NO"

        # Close Database connection
        conn.close()
        st.rerun()
        




# Add a button to navigate back to the home page        
if st.button("Save and Exit"):
    # Save logic here
    st.switch_page("home.py")


if st.button("Reset All Tasks"):
    # Reset all Tasks
    cur = conn.cursor()
    cur.execute("UPDATE Task SET status = 'PENDING', date_completed='' ")    
    conn.commit() 
    conn.close()
    st.rerun()