import streamlit as st
import pandas as pd
import sqlite3 as sql


st.markdown("# Task Data")
st.sidebar.markdown("# Task Data")

if "first_load" not in st.session_state:
    st.session_state.first_load = "YES"

# st.write(st.session_state.first_load)

MyDB = "CS IA DB.db"

# Create DB Connection 
conn = sql.connect(MyDB)

# Read the entire table into a DataFrame
df = pd.read_sql("SELECT * FROM Task", conn)
st.write(df)

# Read subjects
df_subject = pd.read_sql("SELECT subject_id, title FROM Subject", conn)
subject_titles = df_subject['title'].tolist()

with st.form("data_form", clear_on_submit=True):
    subject = st.selectbox("Subject Name:", options = subject_titles)
    selected_subject_id = df_subject.loc[df_subject['title'] == subject, 'subject_id'].iloc[0]
        

    title = st.text_input("Task Title", key="txtTitle")
    deadline = st.text_input("Deadline", key="txtDeadline")
    

    submit = st.form_submit_button("Add Task")


    if submit:

        st.write(selected_subject_id)    
        st.write(subject)
        st.write(title)

        # Create a DataFrame for the new record
        #data_record = [{"subject_id": 0, "title": title}]
        #df_data = pd.DataFrame(data_record)
        

        #cur = conn.cursor()
        #cur.executemany("INSERT INTO Subject VALUES(NULL, :title)", data_record)
        #conn.commit() 

        st.session_state.first_load = "NO"

    

        conn.close()
        #st.rerun()




if st.button("Save and Exit"):
    # Save logic here
    st.switch_page("home.py")




