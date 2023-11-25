import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Data")

# Establishing a Google Sheets connection
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="streamdata", usecols=list(range(3)), ttl=5)
existing_data = existing_data.dropna(how="all")

st.dataframe(existing_data)

with st.form(key="vendor_form"):
    keyid = st.text_input(label="ID*")
    keyname = st.text_input(label="name*")
    keyage = st.text_input(label="age*")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not keyname or not keyage:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        elif existing_data["name"].str.contains(keyname).any():
            st.warning("already exists.")
            st.stop()
        else:
            # Create a new row of vendor data
            vendor_data = pd.DataFrame(
                [
                    {
                        "id": keyid,
                        "name": keyname,
                        "age": keyage,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat(
                [existing_data, vendor_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="streamdata", data=updated_df)

            st.success("successfully submitted!")
