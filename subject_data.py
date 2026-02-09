# Import libraries required for this page
import streamlit as st    # main streamlit library 
import pandas as pd       # pandas library for working and displaying with data 
import sqlite3 as sql     # sqllite3 library to work with a sqllite database


# Display the page title at the top of the page and in the left navigation sidebar
st.markdown("# Subject Data")
st.sidebar.markdown("# Subject Data")

if "first_load" not in st.session_state:
    st.session_state.first_load = "YES"

# Set the variable name for my DB
MyDB = "CS IA DB.db"

# Create DB Connection 
conn = sql.connect(MyDB)

# Read the entire table into a DataFrame
# Create a SQL command to read data from the table 
df = pd.read_sql("SELECT * FROM Subject", conn)
# Display the dataframe on the page
st.write(df)

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

        # Close Database connection           
        conn.close()
        st.rerun()



# Add a button to navigate back to the home page        
if st.button("Save and Exit"):
    st.switch_page("home.py")
    