import streamlit as st 

st.write("My IBDP Computer Science - IA")

# st.write("For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/).")

st.write("hello")
import streamlit as st

# Define the pages
home_page = st.Page("home.py", title="Home", icon="🏠", default=True)
subject_page = st.Page("subject_data.py", title="Subject Data", icon="➕")
task_page = st.Page("task_data.py", title="Task Data", icon="📊")


# Set up navigation
pg = st.navigation([home_page, subject_page, task_page])

# Run the selected page
pg.run()




if st.button("Add New Subject"):
    st.switch_page(subject_page) 