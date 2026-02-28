# Import libraries required for this page
import streamlit as st    # main streamlit library 
import pandas as pd       # pandas library for working and displaying with data 
import sqlite3 as sql     # sqllite3 library to work with sqllite database


# Display the page title at the top of the page and in the left navigation sidebar


st.markdown("# User Data")
st.sidebar.markdown("# User Data")




# Set the variable name for my DB
MyDB = "CS IA DB.db"

# Create DB Connection 
conn = sql.connect(MyDB)

# Read the entire table into a DataFrame
# Create a SQL command to read data from the table 
df = pd.read_sql("SELECT * FROM User", conn)
# Display the dataframe on the page
st.write(df)

# Create a form to enter data
with st.form("data_form", clear_on_submit=True):
    # Add text fields to collect data in each column
    firstname = st.text_input("First Name", key="txtFirstName")  
    lastname = st.text_input("Last Name", key="txtLastName")
    dateofbirth = st.text_input("Date of Birth", key="txtdob")
    username = st.text_input("User Name", key="txtUserName")
    password = st.text_input("Password", key="txtPassword")
    # Add a sumbit button
    submit = st.form_submit_button("Add User")


    # Save the new record into the database
    if submit:
        # Create a DataFrame for the new record
        data_record = [{"user_id":0,   "firstname": firstname, "lastname": lastname, "dateofbirth": dateofbirth, "username":username, "password":password }]
        df_data = pd.DataFrame(data_record)
        

        # Create a SQL command to save the record to the database
        cur = conn.cursor()
        cur.executemany("INSERT INTO User VALUES(NULL,:firstname, :lastname, :dateofbirth, :username, :password)", data_record)
        conn.commit() 

        conn.close()
        st.rerun()

# Add a button to navigate back to the home page        
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