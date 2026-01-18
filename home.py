import streamlit as st
import pandas as pd
import sqlite3 as sql
import datetime as dt
from datetime import datetime as dt

# Home page content
#st.write("IBDP - Computer Science - IA")
st.title("Alei Khorshed's Planning App")


# Displaying at the top of the sidebar
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


# Get no of pending tasks
df_TasksCount = pd.read_sql("SELECT Count(task_id) as total FROM Task Where status='PENDING' ", conn)

if not df_TasksCount.empty:
    task_row = df_TasksCount.iloc[0]
    st.session_state.gNoTasksPending = int(task_row['total'])

# Get no of completed tasks based on date for today
df_TasksCount = pd.read_sql("SELECT Count(task_id) as total FROM Task WHERE status='COMPLETED' AND date_completed = '" + todaygoaldate + "'" ,conn) 
if not df_TasksCount.empty:
    task_row = df_TasksCount.iloc[0]
    st.session_state.gNoTasksCompleted = int(task_row['total'])

# Calculate Progress Points by multiplying each task difficulty by 1, 2 or 3 for all completed tasks today

if st.session_state.gGoalpoints!= 0:
    df_ProgressPoints = pd.read_sql("SELECT * FROM Task WHERE status='COMPLETED' AND date_completed = '" + todaygoaldate + "'" ,conn) 

    if not df_ProgressPoints.empty:
        difficulty_map = {"Easy": 1, "Medium": 2, "Hard": 3}
        total_points = df_ProgressPoints['difficulty'].map(difficulty_map).sum()
        st.session_state.gProgresspoints = total_points
    else:
        st.session_state.gProgresspoints = 0
else:
    st.session_state.gProgresspoints = 0

# Calculate Goal Progress Perc %
if st.session_state.gGoalpoints!= 0:
    ProgPerc = st.session_state.gProgresspoints / st.session_state.gGoalpoints
    st.session_state.gProgressPerc = round(st.session_state.gProgresspoints / st.session_state.gGoalpoints,2)*100
else:
    st.session_state.gProgressPerc = 0


# Display buttons for start and stop working

st.divider()
# Create 6 equal-width columns
col1, col2, col3, col4, col5, col6 = st.columns(6)


with col1:
    if st.button("Start Working"):
        if st.session_state.gGoalpoints != 0:
            st.session_state.gFlagWorking = True
            st.session_state.gCurrentActivity = "WORKING" 
            st.session_state.gEndtime = "00:00:00"
            # Check if first time to start working to get start time  
            if st.session_state.gStarttime == "00:00:00":
                st.session_state.gStarttime = dt.now()
                st.session_state.gStarttimelast = st.session_state.gStarttime
            else:
                st.session_state.gStarttimelast = dt.now()
                st.session_state.gStarttime = dt.now()  # This can be removed to keep start time of whole session fixed
    
        else:
            st.error("You need to first add a goal point for today. Goto Goal Planning")
        

with col2:
    if st.button("Stop Working"):
        if st.session_state.gGoalpoints != 0:
            st.session_state.gFlagWorking = False
            st.session_state.gCurrentActivity = "IDLE"    
            st.session_state.gEndtime = dt.now()  
        else:
            st.error("You need to first add a goal point for today. Goto Goal Planning")
     

with col3:
    if st.button("Goal Planning"):
        st.switch_page("goal_planning.py") 


with col4:
    if st.button("Subject Data"):
        st.switch_page("subject_data.py") 

with col5:
    if st.button("Task Data"):
        st.switch_page("task_data.py") 


with col6:
    if st.button("User Data"):
        st.switch_page("user_data.py") 



def DisplayNumber(label, value):
    # Define a function to display a small title and a large bold dark blue number  
    st.markdown(
        f"""
        <div style="text-align: left; background-color: #E3F2FD; padding: 15px; border-radius: 10px; border: 1px solid #BBDEFB;">
            <p style="font-size: 18px; font-weight: 400; color: #666; margin-bottom: 0px;">{label}</p>
            <p style="font-size: 30px; font-weight: bold; color: #003366; margin-top: -10px;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


@st.fragment(run_every="1s")
def goal_timer():
    if st.session_state.gStarttime:
        # Check if first run 
        if st.session_state.gStarttime !="00:00:00":
            # Check if working
            if st.session_state.gFlagWorking:
                diff = dt.now() - st.session_state.gStarttimelast
            else:
                diff = st.session_state.gEndtime - st.session_state.gStarttimelast

            # Format the difference into Hours:Minutes:Seconds        
            seconds = int(diff.total_seconds()) # total_seconds() gives us the duration
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            elapsed_time = f"{hours:02d}:{minutes:02d}:{secs:02d}"                        
        else:
            elapsed_time = "00:00:00"
    else:
        elapsed_time = "00:00:00"


    st.markdown(
        f"""
        <div style="text-align: left; background-color: #E3F2FD; padding: 15px; border-radius: 10px; border: 1px solid #BBDEFB;">
        <p style="font-size: 18px; font-weight: 400; color: #666; margin-bottom: 0px;">Session Time</p>
        <p style="font-size: 30px; font-weight: bold; color: #003366; margin-top: -10px;">{elapsed_time}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
            #<p style="font-size: 18px; font-weight: 400; color: #000000; margin-bottom: 0px;">Session Time</p>
            #<p style="font-size: 30px; font-weight: bold; color: #003366; margin-top: -10px; font-family: monospace;">{elapsed_time}</p>



st.divider()


# Create 5 columns
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    DisplayNumber("Goal Points", st.session_state.gGoalpoints)

with col2:
    DisplayNumber("Pending Tasks", st.session_state.gNoTasksPending)

with col3:
    DisplayNumber("Completed Tasks", st.session_state.gNoTasksCompleted)

with col4:
    DisplayNumber("Progress Points", st.session_state.gProgresspoints)

with col5:
    DisplayNumber("Progress %", st.session_state.gProgressPerc )

# Display Status of current goal planning
# Create 5 columns
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    DisplayNumber("Current Activity", st.session_state.gCurrentActivity)

with col2:
    if st.session_state.gStarttime:
        if st.session_state.gStarttime!="00:00:00":
            DisplayNumber("Start Time", st.session_state.gStarttime.strftime("%H:%M:%S"))
        else:
            DisplayNumber("Start Time", "00:00:00")            
    else:
        DisplayNumber("Start Time","00:00:00")

with col3:
    if st.session_state.gEndtime:
        if st.session_state.gEndtime !="00:00:00":
            DisplayNumber("End Time", st.session_state.gEndtime.strftime("%H:%M:%S"))
        else:
            DisplayNumber("End Time", "00:00:00")
    else:
        DisplayNumber("End Time","00:00:00")

with col4:
    goal_timer()

with col5:    
    if st.session_state.gProgressPerc >= 100:
        DisplayNumber("Goal Status","COMPLETED")
        
    else:
        DisplayNumber("Goal Status","IN PROGRESS")

st.divider()

st.markdown("## **My PENDING Tasks**")
# Read and display Tasks that are pending
df_task = pd.read_sql("SELECT task_id, title, deadline, difficulty, status, date_completed FROM Task Where status='PENDING' ", conn)


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
        cursor.execute("UPDATE Task SET status = 'COMPLETED', date_completed='" + todaygoaldate + "' WHERE task_id = ?", (int(task_id),))
        conn.commit()
        
        st.success(f"Task '{task_title}' marked as completed!")
        st.rerun() # Refresh page to show updated DB data
else:
    st.write("Please click a row in the table to select a task.")

st.divider()
st.markdown("## **My COMPLETED Tasks**")
# Read and display Tasks that are pending
df_task_completed = pd.read_sql("SELECT task_id, title, deadline, difficulty, status, date_completed FROM Task Where status='COMPLETED' ", conn)
st.write(df_task_completed)


conn.close()
st.rerun()


