import streamlit as st
import pandas as pd
import sqlite3 as sql


st.markdown("# Goal planning")
st.sidebar.markdown("# Goal Planning")

if "first_load" not in st.session_state:
    st.session_state.first_load = "YES"

# st.write(st.session_state.first_load)

MyDB = "CS IA DB.db"

# Create DB Connection 
conn = sql.connect(MyDB)


#st.markdown("## **My Tasks**")
# Read and display Tasks
#df_task = pd.read_sql("SELECT * FROM Task", conn)
#task_titles = df_task['title'].tolist()
#st.write(df_task)

st.markdown("## **My Goal Planning**")
# Read data for Goal points from the database into a DataFrame and display it
df = pd.read_sql("SELECT * FROM GoalPoints", conn)
st.write(df)

with st.form("data_form", clear_on_submit=True):
    goal_date = st.date_input("Today's Date", value="today",format=st.session_state.gDateFormat)
    description = st.text_input("Goal Plan Description", key="txtdescription")
    goal_points = st.slider('Goal Points',0, 100, key="txtGoalPoints")

    submit = st.form_submit_button("Add Goal")


    if submit:

        # Create a DataFrame for the new record
        data_record = [{"goalpoints_id":0, "user_id": st.session_state.gCurrentUser, "description":description, "date":goal_date, "targetpoints":goal_points, "progresspoints":0}]
        #df_data = pd.DataFrame(data_record)
        

        cur = conn.cursor()
        cur.executemany("INSERT INTO GoalPoints VALUES(NULL,:user_id, :date, :description, :targetpoints, :progresspoints)", data_record)
        conn.commit() 

        st.session_state.first_load = "NO"

    
        conn.close()
        st.rerun()
        





if st.button("Save and Exit"):
    # Return to home page
    st.switch_page("home.py")


if st.button("Clear All Goals"):
    # Delete all goals
    cur = conn.cursor()
    cur.execute("Delete * from GoalPoints")
    conn.commit() 
    conn.close()
    st.rerun()

