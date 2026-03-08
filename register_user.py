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
            firstname - firstname.strip()
            lastname - lastname.strip()
            username = username.strip()
            password = password.strip()

            if not firstname or not lastname or not username or not password:   
                # Create a DataFrame for the new record
                data_record = [{"user_id":0,   "firstname": firstname, "lastname": lastname, "dateofbirth": dateofbirth, "username":username, "password":password }]
                df_data = pd.DataFrame(data_record)
                
                # Create a SQL command to save the record to the database
                cur = conn.cursor()
                cur.executemany("INSERT INTO User VALUES(NULL,:firstname, :lastname, :dateofbirth, :username, :password)", data_record)
                conn.commit() 

                # Get the user_id of the user which has been saved into the database

                # Find matchin user in the database
                df_user = pd.read_sql("SELECT * FROM user WHERE username = ? AND password = ?", conn, params=[username , password])
                if not df_user.empty:
                    # Get user_id from the database
                    user_row = df_user.iloc[0]                    
                    st.session_state.gCurrentUser = int(user_row['user_id'])
                    st.session_state.gCurrentUserName = username
                    st.text("user found")
                    st.text(st.session_state.gCurrentUser)
                    #st.switch_page("home.py")

                else:
                    st.session_state.gCurrentUser = 0
                    st.session_state.gCurrentUserName = "Guest"
                    st.switch_page("home.py")

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
