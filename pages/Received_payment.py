import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
from datetime import datetime
import time
from zoneinfo import ZoneInfo

# Display Title and Description
# st.title("Data")

st.set_page_config(
    page_title="Received Pay",
    page_icon="💹",
)
st.write("### Welcome to Received Pay Tracker 📆 💵")

# st.sidebar.success("Select a demo above.")
hide_menu = """
<style>
#MainMenu{
    display:none;
}
.st-emotion-cache-1p1m4ay{
    display:none;
}
.st-emotion-cache-cio0dv{
    display:none;
}

</style>
"""


# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
# conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Received",
                          usecols=list(range(8)), ttl=2)
existing_data = existing_data.dropna(how="all")

st.markdown(hide_menu, unsafe_allow_html=True)


opt = ['GPay', 'Salary AC', 'Cash', 'Other']

with st.form(key="vendor_form"):
    user_s = st.text_input(label="User*", placeholder="Enter your name", value="Ashish Moghe")
    from_s = st.selectbox(label="From*",options=opt)
    to_s = st.selectbox(label="To*",options=opt)
    amount_s = st.number_input(label="Amount*", min_value=1, max_value=1000_000)
    description_s = st.text_area(label="Description*", placeholder="Description..")

    # Mark mandatory fields
    st.markdown("**required*")
    # Getting current date and time
    current_datetime = datetime.now(tz=ZoneInfo("Asia/Kolkata"))

    # Displaying current date and time fields
    st.text(f"Current Date and Time: {current_datetime.strftime('%d-%m-%Y %I:%M %p')}")

    submit_button = st.form_submit_button(label="Submit")

    # If the submit button is pressed
if submit_button:
    # Check if all mandatory fields are filled
    if not description_s or not amount_s or not to_s or not from_s or not user_s:
        st.warning("Ensure all mandatory fields are filled.")
        st.stop()
    else:
        # Split Date_Time into separate Date and Time columns
        # Get the current date in the specified format (DD-MM-YYYY)
        current_date = current_datetime.strftime("%d/%m/%Y")
        current_time = current_datetime.strftime(
            "%I:%M %p")  # 12-hour format with AM/PM

        # Create 'Month' column from the 'Date'
        # Format: Month-Year (e.g., Nov-2023)
        month = current_datetime.strftime("%b-%Y")

        # Create a new row of vendor data
        # Increment serial number based on existing rows
        serial_no = len(existing_data) + 1

    # Create a dictionary for the new record
        new_record = {
            "Sr.No": serial_no,
            "User": user_s,
            "Date": current_date,
            "Month": month,
            "Time": current_time,
            "From": from_s,
            "To": to_s,
            "Amount": amount_s,
            "Description": description_s
        }

        # Append the new record to the existing_data DataFrame
        existing_data = existing_data.append(new_record, ignore_index=True)

        # Update Google Sheets with the updated DataFrame containing all records
        conn.update(worksheet="Received", data=existing_data)
        st.success("Successfully submitted!")
