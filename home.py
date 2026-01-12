import streamlit as st

# Home page content

st.title("QuestMania")
st.write("My Computer Science - IA")

#st.markdown("# Home 🏠")
st.sidebar.markdown("# Home 🏠")



if st.button("Add New Subject"):
    st.switch_page("subject_data.py") 
