import streamlit as st
import pandas as pd
import sqlite3 as sql


st.markdown("# Goal planning")
st.sidebar.markdown("# Goal Planning")

if "first_load" not in st.session_state:
    st.session_state.first_load = "YES"

# st.write(st.session_state.first_load)

MyDB = "CS IA DB.db"

# Create DB Connection 
conn = sql.connect(MyDB)

# Read the entire table into a DataFrame
df = pd.read_sql("SELECT * FROM GoalPoints", conn)
st.write(df)

# Read subjects
df_subject = pd.read_sql("SELECT subject_id, title FROM Subject", conn)
subject_titles = df_subject['title'].tolist()

# Read Tasks
df_task = pd.read_sql("SELECT * FROM Task", conn)
task_titles = df_task['title'].tolist()



with st.form("data_form", clear_on_submit=True):
    todays_date = st.date_input("Today's Date", value="today",format=st.session_state.gDateFormat)
 
    subject = st.selectbox("Subject Name:", options = subject_titles)    
    task = st.selectbox("Task:", options = task_titles)   

    goal_points = st.text_input("Goal Points", key="txtGoalPoints")
 

    submit = st.form_submit_button("Add Goal")


    if submit:
        selected_task_id = int(df_task.loc[df_task['title'] == task, 'task_id'].iloc[0])
        st.write(selected_task_id)    
        st.write(task)
        st.write(goal_points)

        # Create a DataFrame for the new record
        #data_record = [{"task_id":0,   "subject_id": selected_subject_id, "user_id": 0, "title":title, "deadline":deadline, "difficulty":difficulty}]
        #df_data = pd.DataFrame(data_record)
        

        #cur = conn.cursor()
        #cur.executemany("INSERT INTO Task VALUES(NULL,:subject_id, :user_id, :title, :deadline, :difficulty)", data_record)
        #conn.commit() 

        st.session_state.first_load = "NO"

    

        conn.close()
        #st.rerun()
        





if st.button("Save and Exit"):
    # Save logic here
    st.switch_page("home.py")




