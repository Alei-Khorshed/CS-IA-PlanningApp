import streamlit as st 

# Init Session States
st.session_state.gCurrentUser = 1
st.session_state.gDateFormat = "DD/MM/YYYY"

# Init status of goal session
st.session_state.gFlagWorking = False
st.session_state.gCurrentActivity = "NONE"
st.session_state.gStarttime = ""
st.session_state.gEndtime = ""
st.session_state.gTotalSessiontime = ""
st.session_state.gGoalpoints = 0
st.session_state.gProgresspoints = 0


# Define the pages
home_page = st.Page("home.py", title="Home", icon="🏠", default=True)
subject_page = st.Page("subject_data.py", title="Subject Data", icon="➕")
task_page = st.Page("task_data.py", title="Task Data", icon="📊")
goal_planning = st.Page("goal_planning.py", title="Goal Planning", icon="➕")


# Set up navigation
pg = st.navigation([home_page, subject_page, task_page,goal_planning])

# Run the selected page
pg.run()



