import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

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


statusopt = ["Done", "Pending", "Cancelled"]
st.markdown(hide_menu, unsafe_allow_html=True)
with st.form(key="vendor_form"):
    paidby = st.text_input(label="Paid By*")
    content = st.text_input(label="Content*")
    amountpaid = st.text_input(label="Amount Paid*")
    friendcount = st.text_input(label="Friend Count*")
    description = st.text_area(label="Description*")
    status = st.selectbox(label="Status*", options=statusopt)

    # Getting current date and time
    current_datetime = datetime.now(tz=ZoneInfo("Asia/Kolkata"))

    # Displaying current date and time fields
    st.text(
        # f"Current Date and Time: {current_datetime.strftime('%d/%m/%Y %I:%M:%S %p')}")
        f"Current Date and Time: {current_datetime.strftime('%d-%m-%Y %I:%M %p')}")

    # Mark mandatory fields
    st.markdown("**required*")

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
