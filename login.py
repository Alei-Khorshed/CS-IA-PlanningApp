# Import libraries required for this page
import streamlit as st    # main streamlit library 
import pandas as pd       # pandas library for working and displaying with data 
import sqlite3 as sql     # sqllite3 library to work with a sqllite database

 
# *** Function definitions ***

# Function to connect to the database and return a database connection
def get_db_connection() -> sql.Connection:
    # Set the variable name for the database
    TaskDB = st.session_state.gDBName

    # Create DB Connection 
    conn = sql.connect(TaskDB,check_same_thread=False)

    return conn

# Function to display user form 
def login_form(conn : sql.Connection):
    
    # Create a form to enter data
    with st.form("data_form"):
        # Add text fields to collect data in each column
        username = st.text_input("User Name", key="txtUserName")
        password = st.text_input("Password", key="txtPassword", type="password")
        # Add a sumbit button
        submit = st.form_submit_button("Login")
               
        # Search for user in the database based on the username and password
        if submit:
            username = username.strip()
            password = password.strip()
            # Validate that username and password are not both empty
            if not username or not password:                    
                st.error("Enter a username and password")
            else:
                # Check if a matching user is found in the database
                df_user = pd.read_sql("SELECT * FROM user WHERE username = ? AND password = ?", conn, params=[username , password])
                if not df_user.empty:
                    # A matching User has been found so login can proceed
                    # Get user_id from the database
                    user_row = df_user.iloc[0]                    
                    st.session_state.gCurrentUser = int(user_row['user_id'])
                    st.session_state.gCurrentUserName = username
                    st.switch_page("home.py")

                else:
                    st.error("A user matching the above username and password could not be found! If you are a new user click on 'Register New User'. ")
                    st.session_state.gCurrentUser = 0
                    st.session_state.gCurrentUserName = "Guest"

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
    login_form(st.session_state.gDBConnection)

    
    if st.button("Register New User"):
        st.switch_page("register_user.py") 


except Exception as err:
    st.error(f"The following error has occured: {err=}, {type(err)=}")

    