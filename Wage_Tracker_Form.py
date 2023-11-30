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
    page_title="Wage Tracker",
    page_icon="💹",
)
st.write("### Welcome to Daily Wages Tracker 📆 💵")

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
existing_data = conn.read(worksheet="Wage Tracker",
                          usecols=list(range(11)), ttl=5)
existing_data = existing_data.dropna(how="all")


st.markdown(hide_menu, unsafe_allow_html=True)
with st.form(key="vendor_form"):
    paidby = st.text_input(label="Paid By*", placeholder="Enter your name")
    content = st.text_input(
        label="Content*", placeholder="Lunch,Dinner,Breakfast...")
    amountpaid = st.number_input(label="Amount Paid*", max_value=100_000)
    friendcount = st.number_input(label="Friend Count*", max_value=25)
    description = st.text_area(label="Description*", placeholder="Description with Status...")

    # Mark mandatory fields
    st.markdown("**required*")
    # Getting current date and time
    current_datetime = datetime.now(tz=ZoneInfo("Asia/Kolkata"))

    # Displaying current date and time fields
    st.text(
        # f"Current Date and Time: {current_datetime.strftime('%d/%m/%Y %I:%M:%S %p')}")
        f"Current Date and Time: {current_datetime.strftime('%d-%m-%Y %I:%M %p')}")


    submit_button = st.form_submit_button(label="Submit")

    # If the submit button is pressed
if submit_button:
    # Check if all mandatory fields are filled
    if not content or not amountpaid or not description or not friendcount or not paidby:
        st.warning("Ensure all mandatory fields are filled.")
        st.stop()
    else:
        # Convert input fields to appropriate data types
        amount_paid = int(amountpaid)
        friend_count = int(friendcount)

        # Calculate My Share
        my_share = amount_paid / friend_count

        # Calculate Splitted Amount
        splitted_amount = amount_paid - my_share

        my_share = round(my_share)
        splitted_amount = round(splitted_amount)

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
            "Date": current_date,
            "Month": month,
            "Time": current_time,
            "Paid By": paidby,
            "Contents": content,
            "Amount Paid": amount_paid,
            "My Share": my_share,
            "Splitted Amount": splitted_amount,
            "Friend Count": friend_count,
            "Description": description,
            "Output": "Done"
        }

        # Append the new record to the existing_data DataFrame
        existing_data = existing_data.append(new_record, ignore_index=True)

        # Update Google Sheets with the updated DataFrame containing all records
        conn.update(worksheet="Wage Tracker", data=existing_data)

        st.success("Successfully submitted!")
