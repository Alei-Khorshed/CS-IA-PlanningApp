import streamlit as st
import pandas as pd
import sqlite3 as sql
import datetime as dt
from datetime import datetime as dt

# Home page content
st.write("IBDP - Computer Science - IA")
st.title("Alei Khorshed - Planning App")


#st.markdown("# Home 🏠")
st.sidebar.markdown("# Home 🏠")



# Get today's date in a specific format (day, month year)
today = dt.now().strftime("%d, %B %Y")

st.markdown(
    f"""
    <div style="display: flex; align-items: baseline; gap: 15px;">
        <span style="font-size: 42px; font-weight: bold; color: #000000;">Today's Date:</span>
        <span style="font-size: 42px; font-weight: bold; color: #003366;">{today}</span>
    </div>
    """, 
    unsafe_allow_html=True
)

def DisplayNumber(label, value):
    # Define a function to display a small title and a large bold dark blue number  
    st.markdown(
        f"""
        <div style="text-align: left;">
            <p style="font-size: 22px; font-weight: 400; color: #666; margin-bottom: 0px;">{label}</p>
            <p style="font-size: 42px; font-weight: bold; color: #003366; margin-top: -10px;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )



@st.fragment(run_every="1s")
def goal_timer():
    # This specific function will rerun every 1 second
    current_time = dt.now().strftime("%H:%M:%S")
    st.markdown(
        f"""
        <div style="
            display: inline-block;
            padding: 5px 15px;
            border-radius: 5px;
            background-color: #f0f2f6;
            border: 1px solid #d1d5db;
            width: fit-content;
            margin-top: 10px;
        ">
            <span style="font-size: 22px; color: #555; font-weight: bold; margin-right: 10px;">Session Time:</span>
            <span style="font-size: 42px; font-family: monospace; color: #003366; font-weight: bold;">{current_time}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def timer_column():
    current_time = dt.now().strftime("%H:%M:%S")
    st.markdown(
        f"""
        <div style="text-align: left;">
            <p style="font-size: 22px; font-weight: 600; color: #000000; margin-bottom: 0px;">Session Time</p>
            <p style="font-size: 42px; font-weight: bold; color: #003366; margin-top: -10px; font-family: monospace;">{current_time}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# Call the fragment
goal_timer()


st.divider()

# Create 4 columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    DisplayNumber("Current Activity", "NONE")

with col2:
    DisplayNumber("Start Time", "0")

with col3:
    DisplayNumber("End Time", "0")

with col4:
    timer_column()


st.divider()

# Create 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    DisplayNumber("Goal Points", "0")

with col2:
    DisplayNumber("Progress Points", "0")

with col3:
    DisplayNumber("Progress %", "0.8%")




st.divider()
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


