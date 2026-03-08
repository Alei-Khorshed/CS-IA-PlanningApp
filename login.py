# Import libraries required for this page
import streamlit as st    # main streamlit library 
import pandas as pd       # pandas library for working and displaying with data 
import sqlite3 as sql     # sqllite3 library to work with a sqllite database
import datetime as dt     # datetime library to manage start and end of session
from datetime import datetime as dt


 
# *** Function definitions ***

# Function to connect to the database and return a database connection
def get_db_connection() -> sql.Connection:
    # Set the variable name for the database
    TaskDB = st.session_state.gDBName

    # Create DB Connection 
    conn = sql.connect(TaskDB,check_same_thread=False)

    return conn

# Function to display user form 
def display_login_form(conn : sql.Connection):
    
    # Create a form to enter data
    with st.form("data_form", clear_on_submit=True):
        # Add text fields to collect data in each column
        username = st.text_input("User Name", key="txtUserName")
        password = st.text_input("Password", key="txtPassword")
        # Add a sumbit button
        submit = st.form_submit_button("Login")


        # Save the new record into the database
        if submit:
            # Create a SQL command to save the record to the database
            cur = conn.cursor()
            cur.executemany("INSERT INTO User VALUES(NULL,:firstname, :lastname, :dateofbirth, :username, :password)", data_record)
            conn.commit() 
            st.rerun()

    return
# *** Main page code ***

# Create error handling 
try:

    # Home page content
    st.title("Questmania Planning App")


    # Create DB connection
    if "gDBConnection" not in st.session_state:
        st.session_state.gDBConnection = get_db_connection()

    # Display the subject data form
    display_login_form(st.session_state.gDBConnection)


    st.divider()
    # Create 2 equal-width columns
    col1, col2  = st.columns(2)

  
    with col1:
        if st.button("Login"):
            st.switch_page("login.py") 

    with col2:
        if st.button("Register New User"):
            st.switch_page("register_user.py") 


 


except Exception as err:
    st.error(f"The following error has occured: {err=}, {type(err)=}")
    