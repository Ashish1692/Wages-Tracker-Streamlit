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
btn_stl=""" 
<style>
.stButton > Button{
    backgound-color:orange;
    width: 100%;
    text-align: center;
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


statusopt = ["Done", "Pending", "Cancelled"]
st.markdown(hide_menu, unsafe_allow_html=True)
with st.form(key="vendor_form"):
    paidby = st.text_input(label="Paid By*",placeholder="Enter your name")
    content = st.text_input(label="Content*",placeholder="Lunch,Dinner,Breakfast...")
    amountpaid = st.number_input(label="Amount Paid*",max_value=100_000)
    friendcount = st.number_input(label="Friend Count*",max_value=25)
    description = st.text_area(label="Description*",placeholder="Decsribe your content...")
    status = st.selectbox(label="Status*", options=statusopt)

    # Getting current date and time
    current_datetime = datetime.now(tz=ZoneInfo("Asia/Kolkata"))

    # Displaying current date and time fields
    st.text(
        # f"Current Date and Time: {current_datetime.strftime('%d/%m/%Y %I:%M:%S %p')}")
        f"Current Date and Time: {current_datetime.strftime('%d-%m-%Y %I:%M %p')}")

    # Mark mandatory fields
    st.markdown("**required*")
    st.markdown(btn_stl,unsafe_allow_html=True);
    submit_button = st.form_submit_button(label="Submit")

    # If the submit button is pressed
if submit_button:
    # Check if all mandatory fields are filled
    if not content or not amountpaid or not status or not description or not friendcount or not paidby:
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
        current_time = current_datetime.strftime("%I:%M %p")  # 12-hour format with AM/PM

        # Create 'Month' column from the 'Date'
        # Format: Month-Year (e.g., Nov-2023)
        month = current_datetime.strftime("%b-%Y")

        # Create a new row of vendor data
        # Increment serial number based on existing rows
        serial_no = len(existing_data) + 1
        vendor_data = pd.DataFrame([
            {
                "Sr.No": serial_no,
                "Date": current_date,
                "Month": month,  # Add the 'Month' column
                "Time": current_time,
                "Paid By": paidby,
                "Contents": content,
                "Amount Paid": amount_paid,
                "My Share": my_share,
                "Splitted Amount": splitted_amount,
                "Friend Count": friend_count,
                "Description": description,
                "Status": status
            }
        ])

        # Add the new vendor data to the existing data
        updated_df = pd.concat(
            [existing_data, vendor_data], ignore_index=True)

        # Update Google Sheets with the new vendor data
        conn.update(worksheet="Wage Tracker", data=updated_df)

        st.success("Successfully submitted!")
