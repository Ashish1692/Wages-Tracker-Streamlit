import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing data from Google Sheet
existing_data = conn.read(worksheet="Wage Tracker",
                          usecols=list(range(12)), ttl=5)
existing_data = existing_data.dropna(how="all")

df = pd.DataFrame(existing_data)


hide_menu = """
<style>
.st-emotion-cache-zq5wmm{
    display:none;
}
.st-emotion-cache-cio0dv{
    display:none;
}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)


def search_row():
    st.title('Search Row')

    col_to_search = st.selectbox('Select column to search', df.columns)
    search_value = st.text_input('Enter value to search')

    if st.button('Search'):
        search_result = df[df[col_to_search].astype(
            str).str.contains(search_value)]
        if search_result.empty:
            st.warning('No matching row found.')
        else:
            st.success('Matching rows found:')
            st.write(search_result)


# Function to update existing row values and update the Google Sheet


def update_existing_row():
    st.subheader('Update Existing Row')
    index = st.number_input('Enter row index to update',
                            min_value=0, max_value=len(df) - 1, value=0)
    col_name = st.selectbox('Select column to update', df.columns)
    new_value = st.text_input('Enter new value')

    if st.button('Update'):
        df.at[index, col_name] = new_value
        conn.update(worksheet="Wage Tracker", data=df)
        st.success('Row updated successfully!')

# Function to view sheet data


def view_data():
    st.subheader('View Data')
    st.write(df)


# Streamlit App
st.title('Update Existing Row in Google Sheet')
st.markdown("---")

if st.checkbox('Search for Row'):
    search_row()


update_existing_row()
