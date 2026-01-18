import streamlit as st
import pandas as pd
import sqlite3 as sql


st.markdown("# User Data")
st.sidebar.markdown("# User Data")

MyDB = "CS IA DB.db"

# Create DB Connection 
conn = sql.connect(MyDB)

# Read the entire table into a DataFrame
df = pd.read_sql("SELECT * FROM User", conn)
st.write(df)

with st.form("data_form", clear_on_submit=True):

    firstname = st.text_input("First Name", key="txtFirstName")
    lastname = st.text_input("Last Name", key="txtLastName")
    dob = st.date_input("Date of Birth",min_value="01.01.1970", format=st.session_state.gDateFormat,key="txtDOB")
    username = st.text_input("User Name", key="txtUserName")
    password = st.text_input("Password", key="txtPassword")
    
    submit = st.form_submit_button("Add User")


    if submit:
        # Create a DataFrame for the new record
        data_record = [{"user_id":0,   "firstname": firstname, "lastname": lastname, "dateofbirth": dob, "username":username, "password":password }]
        df_data = pd.DataFrame(data_record)
        

        cur = conn.cursor()
        cur.executemany("INSERT INTO User VALUES(NULL,:firstname, :lastname, :datofbirth, :username, :password", data_record)
        conn.commit() 

        conn.close()
        st.rerun()
        
if st.button("Save and Exit"):
    # Save logic here
    st.switch_page("home.py")


if st.button("Clear All Users"):
    # Delete all Users
    cur = conn.cursor()
    cur.execute("Delete from User") 
    conn.commit() 
    conn.close()
    st.rerun()