# Import libraries required for this page
import streamlit as st    # main streamlit library 
import pandas as pd       # pandas library for working and displaying with data 
import sqlite3 as sql     # sqllite3 library to work with sqllite database


  
# *** Function definitions ***

# Function to connect to the database and return a database connection
def get_db_connection() -> sql.Connection:
    # Set the variable name for the database
    TaskDB = st.session_state.gDBName

    # Create DB Connection 
    conn = sql.connect(TaskDB,check_same_thread=False)

    return conn

# Function to display user form 
def display_user_form(conn : sql.Connection):
    # Create a form to enter data
    with st.form("data_form" ):
        # Add text fields to collect data in each column
        firstname = st.text_input("First Name", key="txtFirstName")  
        lastname = st.text_input("Last Name", key="txtLastName")
        dateofbirth = st.text_input("Date of Birth", key="txtdob")
        username = st.text_input("User Name", key="txtUserName")
        password = st.text_input("Password", key="txtPassword", type="password")
        # Add a sumbit button
        submit = st.form_submit_button("Register User")


        # Save the new record into the database
        if submit:

            # Check that main input is not empty
            firstname = firstname.strip()
            lastname = lastname.strip()
            username = username.strip()
            password = password.strip()

            if not firstname or not lastname or not username or not password:   
                st.error("Enter all the missing form fields.")    


    return


 # *** Main page code ***

# Create error handling 
try:
    # Display the page title at the top of the page 
    st.markdown("# Register New User")

    # Create DB connection
    if "gDBConnection" not in st.session_state:
        st.session_state.gDBConnection = get_db_connection()

    # Display the user data form
    display_user_form(st.session_state.gDBConnection)


except Exception as err:
    st.error(f"The following error has occured: {err=}, {type(err)=}")
