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
today = dt.now().strftime("%d %B %Y")

st.markdown(
    f"""
    <div style="display: flex; align-items: baseline; gap: 15px;">
        <span style="font-size: 30px; font-weight: bold; color: #000000;">Today's Date:</span>
        <span style="font-size: 30px; font-weight: bold; color: #003366;">{today}</span>
    </div>
    """, 
    unsafe_allow_html=True
)



# Create DB Connection 
MyDB = "CS IA DB.db"

conn = sql.connect(MyDB)

#cur = conn.cursor()
#cur.execute("ALTER TABLE GoalPoints ADD COLUMN description TEXT")
#conn.commit() 

# Read information about todays GloalPoints 

todaygoaldate = dt.now().strftime("%Y-%m-%d") 
df_GoalPointsToday = pd.read_sql("SELECT * FROM GoalPoints WHERE date = ?", conn, params=[todaygoaldate])

if not df_GoalPointsToday.empty:
    goal_row = df_GoalPointsToday.iloc[0]

    st.session_state.gGoalpoints = int(goal_row['targetpoints'])
    st.session_state.gProgresspoints = int(goal_row['progresspoints'])
    goal_desc = goal_row['description']
    st.markdown(
        f"""
        <div style="display: flex; align-items: baseline; gap: 15px;">
            <span style="font-size: 30px; font-weight: bold; color: #000000;">My Goal:</span>
            <span style="font-size: 30px; font-weight: bold; color: #003366;">{goal_desc}</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

else:
    # 5. Handle the case where no row exists for today
    #st.status("No goal set for today yet.")
    st.session_state.gGoalpoints = 0
    st.session_state.gProgresspoints = 0
    goal_desc = "NONE"
    st.markdown(
        f"""
        <div style="display: flex; align-items: baseline; gap: 15px;">
            <span style="font-size: 30px; font-weight: bold; color: #000000;">My Goal:</span>
            <span style="font-size: 30px; font-weight: bold; color: #003366;">{goal_desc}</span>
        </div>
        """, 
        unsafe_allow_html=True
    )    


# Get no of pending and completed tasks
df_TasksCount = pd.read_sql("SELECT Count(task_id) as total FROM Task Where status='PENDING' ", conn)

if not df_TasksCount.empty:
    task_row = df_TasksCount.iloc[0]
    st.session_state.gNoTasksPending = int(task_row['total'])

df_TasksCount = pd.read_sql("SELECT Count(task_id) as total FROM Task Where status='COMPLETED' ", conn)
if not df_TasksCount.empty:
    task_row = df_TasksCount.iloc[0]
    st.session_state.gNoTasksCompleted = int(task_row['total'])






st.divider()
# Create 3 equal-width columns
col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    if st.button("Start Working"):
        if st.session_state.gGoalpoints != 0:
            st.session_state.gFlagWorking = True
            st.session_state.gCurrentActivity = "WORKING"   
            st.session_state.gStarttime = dt.now()
        else:
            st.warning("You need to first add a goal point for today. Goto Goal Planning")
        

with col2:
    if st.button("Stop Working"):
        st.session_state.gFlagWorking = False
        st.session_state.gCurrentActivity = "IDLE"    
        st.session_state.gEndtime = dt.now()  



with col3:
    if st.button("Subject Data"):
        st.switch_page("subject_data.py") 

with col4:
    if st.button("Task Data"):
        st.switch_page("task_data.py") 


with col5:
    if st.button("Goal Planning"):
        st.switch_page("goal_planning.py") 




def DisplayNumber(label, value):
    # Define a function to display a small title and a large bold dark blue number  
    st.markdown(
        f"""
        <div style="text-align: left;">
            <p style="font-size: 18px; font-weight: 400; color: #666; margin-bottom: 0px;">{label}</p>
            <p style="font-size: 30px; font-weight: bold; color: #003366; margin-top: -10px;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


@st.fragment(run_every="60s")
def goal_timer():
    if st.session_state.gFlagWorking and st.session_state.gStarttime:
        #current_time = dt.now().strftime("%H:%M:%S")
        diff = dt.now() - st.session_state.gStarttime
        # Format the difference into Hours:Minutes:Seconds        
        seconds = int(diff.total_seconds()) # total_seconds() gives us the duration
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        elapsed_time = f"{hours:02d}:{minutes:02d}:{secs:02d}"        
    else:
        #current_time = ""
        elapsed_time = "00:00:00"
    st.markdown(
        f"""
        <div style="text-align: left;">
            <p style="font-size: 18px; font-weight: 400; color: #000000; margin-bottom: 0px;">Session Time</p>
            <p style="font-size: 30px; font-weight: bold; color: #003366; margin-top: -10px; font-family: monospace;">{elapsed_time}</p>
        </div>
        """,
        unsafe_allow_html=True
    )



st.divider()


# Create 5 columns
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    DisplayNumber("Goal Points", st.session_state.gGoalpoints)

with col2:
    DisplayNumber("Progress Points", st.session_state.gProgresspoints)

with col3:
    DisplayNumber("Progress %", "0%")

with col4:
    DisplayNumber("Pending Tasks", st.session_state.gNoTasksPending)

with col5:
    DisplayNumber("Completed Tasks", st.session_state.gNoTasksCompleted)


# Display Status of current goal planning
# Create 5 columns
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    DisplayNumber("Current Activity", st.session_state.gCurrentActivity)

with col2:
    if st.session_state.gStarttime:
        DisplayNumber("Start Time", st.session_state.gStarttime.strftime("%H:%M:%S"))
    else:
        DisplayNumber("Start Time","00:00:00")

with col3:
    if st.session_state.gEndtime:
        DisplayNumber("End Time", st.session_state.gEndtime.strftime("%H:%M:%S"))
    else:
        DisplayNumber("End Time","00:00:00")

with col4:
    goal_timer()

with col5:
    st.write("")




if "first_load" not in st.session_state:
    st.session_state.first_load = "YES"

st.markdown("## **My Tasks**")
# Read and display Tasks that are pending
df_task = pd.read_sql("SELECT * FROM Task Where status='PENDING' ", conn)
#task_titles = df_task['title'].tolist()
#st.write(df_task)


# Display the Tasks in a dataframe with ROW SELECTION enabled
# 'on_select="rerun"' makes the app reactive when a row is clicked
event = st.dataframe(
    df_task, 
    use_container_width=True, 
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row" 
)

# Handle the selection logic
selected_rows = event.selection.rows

if len(selected_rows) > 0:
    # Get the actual data of the selected row
    row_index = selected_rows[0]
    task_id = df_task.iloc[row_index]['task_id'] 
    task_title = df_task.iloc[row_index]['title']

    st.info(f"Selected Task: **{task_title}**")

    if st.button("Mark Task Completed"):
        # 4. Execute the Update Query
        cursor = conn.cursor()
        cursor.execute("UPDATE Task SET status = 'COMPLETED' WHERE task_id = ?", (int(task_id),))
        conn.commit()
        
        st.success(f"Task '{task_title}' marked as completed!")
        st.rerun() # Refresh page to show updated DB data
else:
    st.write("Please click a row in the table to select a task.")




st.markdown("## **My Goal Planning**")
# Read data for Goal points from the database into a DataFrame and display it
df = pd.read_sql("SELECT * FROM GoalPoints", conn)
st.write(df)
    
conn.close()
st.rerun()


