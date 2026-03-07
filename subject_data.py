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
    conn = sql.connect(TaskDB)

    return conn

# Function to display subject form to load and display subject data and add new subjects
def display_subject_form(conn : sql.Connection):
    # Read the entire table into a DataFrame
    # Create a SQL command to read data from the table 
    df = pd.read_sql("SELECT title FROM Subject", conn)
    # Display the dataframe on the page
    st.dataframe(df , hide_index=True)

    # Create a form to enter data
    with st.form("data_form", clear_on_submit=True):
        title = st.text_input("Subject Title", key="txtTitle")
        # Add a sumbit button
        submit = st.form_submit_button("Add Subject")

        # Save the new record into the database
        if submit:
            # Create a DataFrame for the new record
            #data_record = [{"subject_id": id, "title": title}]
            data_record = [{"subject_id": 0, "title": title}]
            df_data = pd.DataFrame(data_record)
            
            # Write to SQLite
            # 'append' adds to the table; 'replace' would overwrite it        
            #df_data.to_sql("Subject", conn, if_exists="append", index=False)
            

            # Create a SQL command to save the record to the database
            cur = conn.cursor()
            cur.executemany("INSERT INTO Subject VALUES(NULL, :title)", data_record)
            # Commit Database to save changes
            conn.commit() 

            st.session_state.first_load = "NO"

            st.rerun()

    return

# Function to delete all subject data
def delete_subject_data(conn):

    # Delete all records
    cur = conn.cursor()
    conn.execute("DELETE FROM Subject ")    
    conn.gDBConnection.commit() 
    st.rerun()


 # *** Main page code ***

# Create error handling 
try:
    # Display the page title at the top of the page and in the left navigation sidebar
    st.markdown("# Subject Data")
    st.sidebar.markdown("# Subject Data")

    # Create DB connection
    if "gDBConnection" not in st.session_state:
        st.session_state.gDBConnection = get_db_connection()

    # Display the subject data form
    display_subject_form(st.session_state.gDBConnection)


    # Add a button to navigate back to the home page        
    if st.button("Save and Exit"):
        st.switch_page("home.py")

    # Button to delete and reset all records
    if st.button("DELETE ALL Subjects"):
        delete_subject_data(st.session_state.gDBConnection)

except Exception as err:
    st.error(f"The following error has occured: {err=}, {type(err)=}")
    
