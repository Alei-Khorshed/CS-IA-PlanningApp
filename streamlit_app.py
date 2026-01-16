import streamlit as st 

st.set_page_config(layout="wide")
st.markdown("""
    <style>
           .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }
    </style>
    """, unsafe_allow_html=True)


if "gCurrentUser" not in st.session_state:
    st.session_state.gCurrentUser = 1

if "gDateFormat" not in st.session_state:
    st.session_state.gDateFormat = "DD/MM/YYYY"

if "gFlagWorking" not in st.session_state:
    st.session_state.gFlagWorking = False

if "gCurrentActivity" not in st.session_state:
    st.session_state.gCurrentActivity = "IDLE"

if "gStarttime" not in st.session_state:
    st.session_state.gStarttime = ""

if "gEndtime" not in st.session_state:
    st.session_state.gEndtime = ""

if "gTotalSessiontime" not in st.session_state:
    st.session_state.gTotalSessiontime = ""

if "gGoalpoints" not in st.session_state:
    st.session_state.gGoalpoints = 0

if "gProgresspoints" not in st.session_state:
    st.session_state.gProgresspoints = 0

if "gNoTasksPending" not in st.session_state:
    st.session_state.gNoTasksPending = 0

if "gNoTasksCompleted" not in st.session_state:
    st.session_state.gNoTasksCompleted = 0


# Define the pages
home_page = st.Page("home.py", title="Home", icon="🏠", default=True)
subject_page = st.Page("subject_data.py", title="Subject Data", icon="➕")
task_page = st.Page("task_data.py", title="Task Data", icon="➕")
goal_planning = st.Page("goal_planning.py", title="Goal Planning", icon="📊")


# Set up navigation
pg = st.navigation([home_page, subject_page, task_page,goal_planning])

# Run the selected page
pg.run()



