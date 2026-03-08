import streamlit as st 

st.set_page_config(layout="wide")

# Initialize global state variables to be used in the pages of the application

if "gDBName" not in st.session_state:
    st.session_state.gDBName = "TaskDB.db"

if "gCurrentUser" not in st.session_state:
    st.session_state.gCurrentUser = 0

if "gCurrentUserName" not in st.session_state:
    st.session_state.gCurrentUserName = "Guest"

if "gDateFormat" not in st.session_state:
    st.session_state.gDateFormat = "DD/MM/YYYY"

if "gFlagWorking" not in st.session_state:
    st.session_state.gFlagWorking = False

if "gCurrentActivity" not in st.session_state:
    st.session_state.gCurrentActivity = "IDLE"

if "gStarttime" not in st.session_state:
    st.session_state.gStarttime = "00:00:00"

if "gStarttimelast" not in st.session_state:
    st.session_state.gStarttimelast = "00:00:00"

if "gEndtime" not in st.session_state:
    st.session_state.gEndtime = "00:00:00"

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
login = st.Page("login.py", title="Login", default=True)
home_page = st.Page("home.py", title="Home")
goal_planning = st.Page("goal_planning.py", title="Goal Planning")
subject_page = st.Page("subject_data.py", title="Subject Data" )
task_page = st.Page("task_data.py", title="Task Data")
user_page = st.Page("user_data.py", title="User Data")


st.sidebar.markdown(f"### User: **{st.session_state.gCurrentUserName}**")
st.sidebar.divider() # Adds a horizontal line

sidebar_pages = [login, home_page, goal_planning, subject_page, task_page, user_page]

# Set up navigation
pg = st.navigation(sidebar_pages)

# Show selected sidebar page
pg.run()




