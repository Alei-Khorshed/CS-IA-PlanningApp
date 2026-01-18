import streamlit as st 

st.set_page_config(layout="wide")

if "gCurrentUser" not in st.session_state:
    st.session_state.gCurrentUser = 1

if "gCurrentUsername" not in st.session_state:
    st.session_state.gCurrentUsername = "Alei Khorshed"

if "gDateFormat" not in st.session_state:
    st.session_state.gDateFormat = "DD/MM/YYYY"

if "gFlagWorking" not in st.session_state:
    st.session_state.gFlagWorking = False

if "gCurrentActivity" not in st.session_state:
    st.session_state.gCurrentActivity = "IDLE"

if "gStarttime" not in st.session_state:
    st.session_state.gStarttime = ""

if "gStarttimelast" not in st.session_state:
    st.session_state.gStarttimelast = ""

if "gEndtime" not in st.session_state:
    st.session_state.gEndtime = ""

if "gTotalSessiontime" not in st.session_state:
    st.session_state.gTotalSessiontime = ""

if "gGoalpoints" not in st.session_state:
    st.session_state.gGoalpoints = 0

if "gProgresspoints" not in st.session_state:
    st.session_state.gProgresspoints = 0

if "gProgressPerc" not in st.session_state:
    st.session_state.gProgressPerc = 0


if "gNoTasksPending" not in st.session_state:
    st.session_state.gNoTasksPending = 0

if "gNoTasksCompleted" not in st.session_state:
    st.session_state.gNoTasksCompleted = 0


# Define the pages
home_page = st.Page("home.py", title="Home", icon="🏠", default=True)
goal_planning = st.Page("goal_planning.py", title="Goal Planning", icon="📊")
subject_page = st.Page("subject_data.py", title="Subject Data", icon="➕")
task_page = st.Page("task_data.py", title="Task Data", icon="➕")
user_page = st.Page("user_data.py", title="User Data", icon="➕")


st.write(st.session_state.gCurrentUsername)

# Set up navigation
pg = st.navigation([home_page, goal_planning,subject_page, task_page,user_page])

# Run the selected page
pg.run()



