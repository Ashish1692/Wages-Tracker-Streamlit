import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="WAGES DATA", page_icon="📄")
st.markdown("### WAGES DATA")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing data from Google Sheets
existing_data = conn.read(worksheet="Wage Tracker",
                          usecols=list(range(12)), ttl=5)
existing_data = existing_data.dropna(how="all")

st.dataframe(existing_data)
