import streamlit as st

st.markdown("# Subject Data ❄️")
st.sidebar.markdown("# Subject Data ❄️")



if st.button("Save and Exit"):
    # Save logic here
    st.switch_page("streamlit_app.py")
    