import streamlit as st

# Home page content

st.title("Alei Khorshed - Planning App")
st.write("IBDP - Computer Science - IA")

#st.markdown("# Home 🏠")
st.sidebar.markdown("# Home 🏠")



if st.button("Subject Data"):
    st.switch_page("subject_data.py") 

if st.button("Task Data"):
    st.switch_page("task_data.py") 
