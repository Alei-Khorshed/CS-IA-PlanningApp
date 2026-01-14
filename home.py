import streamlit as st
import pandas as pd
import sqlite3 as sql

# Home page content


st.title("Alei Khorshed - Planning App")
st.markdown("## **(IBDP - Computer Science - IA)**")


#st.markdown("# Home 🏠")
st.sidebar.markdown("# Home 🏠")


# Create 3 equal-width columns
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Subject Data"):
        st.switch_page("subject_data.py") 

with col2:
    if st.button("Task Data"):
        st.switch_page("task_data.py") 


with col3:
    if st.button("Goal Planning"):
        st.switch_page("goal_planning.py") 



MyDB = "CS IA DB.db"

# Create DB Connection 
conn = sql.connect(MyDB)

#cur = conn.cursor()
#cur.execute("ALTER TABLE GoalPoints ADD COLUMN description TEXT")
#conn.commit() 


if "first_load" not in st.session_state:
    st.session_state.first_load = "YES"

st.markdown("## **My Tasks**")
# Read and display Tasks
df_task = pd.read_sql("SELECT * FROM Task", conn)
task_titles = df_task['title'].tolist()
st.write(df_task)

st.markdown("## **My Goal Planning**")
# Read data for Goal points from the database into a DataFrame and display it
df = pd.read_sql("SELECT * FROM GoalPoints", conn)
st.write(df)
    
conn.close()
st.rerun()


