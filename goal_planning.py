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

# Function to display goal planning form to load and display goal data and add new goals
def display_goal_planning_form(conn : sql.Connection):

    # Read data for Goal points from the database into a DataFrame and display it
    # Create a SQL command to read data 
    df = pd.read_sql("SELECT date,description,targetpoints,progresspoints FROM GoalPoints", conn)
    st.dataframe(df , hide_index=True)

    # Create a form to enter data
    with st.form("data_form", clear_on_submit=True):
        goal_date = st.date_input("Today's Date", value="today",format=st.session_state.gDateFormat)
        description = st.text_input("Goal Plan Description", key="txtdescription")
        goal_points = st.slider('Goal Points',0, 30, key="txtGoalPoints")
        # Add a sumbit button
        submit = st.form_submit_button("Add Goal")

        # Save the new record into the database
        if submit:

            # Create a DataFrame for the new record
            data_record = [{"goalpoints_id":0, "user_id": st.session_state.gCurrentUser, "description":description, "date":goal_date, "targetpoints":goal_points, "progresspoints":0}]
            #df_data = pd.DataFrame(data_record)
            
            # Create a SQL command to save the record to the database
            cur = conn.cursor()
            cur.executemany("INSERT INTO GoalPoints VALUES(NULL,:user_id, :date, :description, :targetpoints, :progresspoints)", data_record)
            # Commit Database to save changes
            conn.commit() 

            st.session_state.first_load = "NO"
            
            st.rerun()

    return

# Function to delete all goal planning data
def delete_goal_data(conn):
    # Delete all goals
    cur = conn.cursor()
    cur.execute("Delete from GoalPoints")
    conn.commit() 
    st.rerun()
    return



 # *** Main page code ***

# Create error handling 
try:

    # Display the page title at the top of the page and in the left navigation sidebar
    st.markdown("# Goal planning")
    st.sidebar.markdown("# Goal Planning")

    st.markdown("## **My Goal Planning**")

    # Create DB connection
    if "gDBConnection" not in st.session_state:
        st.session_state.gDBConnection = get_db_connection()

    # Display the goal planning data form
    display_goal_planning_form(st.session_state.gDBConnection)

    if st.button("Save and Exit"):
        # Return to home page
        st.switch_page("home.py")


    if st.button("Clear All Goals"):
        delete_goal_data(st.session_state.gDBConnection)

except Exception as err:
    st.error(f"The following error has occured: {err=}, {type(err)=}")