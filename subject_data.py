import streamlit as st
import pandas as pd
import numpy as np

import sqlite3 as sql

st.markdown("# Subject Data ❄️")
st.sidebar.markdown("# Subject Data ❄️")




MyDB = "CS IA DB.db"

# Create DB Connection 
conn = sql.connect(MyDB)


with st.form("data_form"):
    title = st.text_input("Subject Title", key="txtTitle")
    #id = st.number_input("id", min_value=0, max_value=120)
    submit = st.form_submit_button("Add Subject")
    
    if submit:
        # Create a DataFrame for the new record
        #data_record = [{"subject_id": id, "title": title}]
        data_record = [{"subject_id": 0, "title": title}]
        df_data = pd.DataFrame(data_record)
        
        # Write to SQLite
        # 'append' adds to the table; 'replace' would overwrite it        
        #df_data.to_sql("Subject", conn, if_exists="append", index=False)
        


        cur = conn.cursor()
        cur.executemany("INSERT INTO Subject VALUES(NULL, :title)", data_record)
        conn.commit() 



        # Read the entire table into a DataFrame
        df = pd.read_sql("SELECT * FROM Subject", conn)
        st.write(df)
        #st.dataframe(df)

        st.session_state["txtTitle"] = ""

        conn.close()



if st.button("Save and Exit"):
    # Save logic here
    st.switch_page("home.py")
    