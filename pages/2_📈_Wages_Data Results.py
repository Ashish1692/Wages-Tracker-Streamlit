import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Expense Summary", page_icon="📈")

st.markdown("# Expense Summary")

# Establishing a Google Sheets connection
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

existing_data_res = conn.read(
    worksheet="Wage Tracker", usecols=list(range(12)), ttl=5)
existing_data_res = existing_data_res.dropna(how="all")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Monthly", "Content Wise", "Date Wise", "Total Sums"])

with tab1:
    # Grouping data for month-wise total amount
    monthly_total = existing_data_res.groupby(
        'Month')['Amount Paid'].sum().reset_index()

    # Calculate total sum for 'Amount Paid' and add it as a new row in monthly_total DataFrame
    total_monthly_amount = monthly_total['Amount Paid'].sum()
    total_monthly_row = {'Month': 'Total', 'Amount Paid': total_monthly_amount}
    monthly_total = monthly_total.append(total_monthly_row, ignore_index=True)
    # Streamlit app
    st.markdown('#### Total Amount Spent Monthly')
    st.write(monthly_total)

with tab2:
    # Grouping data for content-wise total amount
    content_total = existing_data_res.groupby(
        'Contents')['Amount Paid'].sum().reset_index()

    # Calculate total sum for 'Amount Paid' and add it as a new row in content_total DataFrame
    total_content_amount = content_total['Amount Paid'].sum()
    total_content_row = {'Contents': 'Total',
                         'Amount Paid': total_content_amount}
    content_total = content_total.append(total_content_row, ignore_index=True)
    st.markdown('#### Total Amount Spent by Content')
    st.write(content_total)

with tab3:
    # Convert 'Date' column to datetime format if not already in datetime
    existing_data_res['Date'] = pd.to_datetime(existing_data_res['Date'])

    # Modify 'Date' column to the desired format (24 Nov 2023)
    existing_data_res['Date'] = existing_data_res['Date'].dt.strftime(
        '%d %b %Y')

    # Grouping data for date-wise total amount paid
    datewise_total = existing_data_res.groupby(
        'Date')['Amount Paid'].sum().reset_index()

    # Calculate total sum for 'Amount Paid' and add it as a new row in datewise_total DataFrame
    total_amount_paid = datewise_total['Amount Paid'].sum()
    total_row = {'Date': 'Total', 'Amount Paid': total_amount_paid}
    datewise_total = datewise_total.append(total_row, ignore_index=True)

    st.markdown('#### Total Amount Spent on Each Date')
    st.write(datewise_total)

with tab4:
    # Calculating total sum of 'Amount Paid', 'My Share', 'Splitted Amount'
    total_amount_paid = existing_data_res['Amount Paid'].sum()
    total_my_share = existing_data_res['My Share'].sum()
    total_splitted_amount = existing_data_res['Splitted Amount'].sum()
    # Streamlit app
    st.markdown('#### Total Sum of Amounts')
    st.write(f"Total Amount Paid: {total_amount_paid}")
    st.write(f"Total My Share: {total_my_share}")
    st.write(f"Total Splitted Amount: {total_splitted_amount}")
