# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 08:15:09 2025

@author: jdevore
"""

import streamlit as st
import pandas as pd
from Calculator import add_two_to_numbers
from io import BytesIO

st.set_page_config(layout="wide", page_title="Excel A1 Reader & Calculator")

st.write("## Upload an Excel File for Processing")

# File uploader (moved from sidebar to main page)
uploaded_file = st.file_uploader("### 📤 Drag and drop or browse to upload an Excel file (.xlsx)", type=["xlsx"])

# Dropdown menu (moved below the uploader)
option = st.selectbox(
    "Choose an action to perform:",
    ("Read cell A1", "Preview sheet", "Show entire file", "Add 2 to all numbers"),
    index=0
)

# Excel processing
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=None)

        if option == "Read cell A1":
            value_a1 = df.iloc[0, 0]
            st.success(f"Value in cell A1: `{value_a1}`")

        elif option == "Preview sheet":
            st.write("### Preview of the first 10 rows:")
            st.dataframe(df.head(10))

        elif option == "Show entire file":
            st.write("### Entire Excel Sheet:")
            st.dataframe(df)

        elif option == "Add 2 to all numbers":
            modified_df = add_two_to_numbers(df)
            st.write("### Modified DataFrame (2 added to all numeric cells):")
            st.dataframe(modified_df)

            # Create a download link for the modified file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                modified_df.to_excel(writer, index=False, header=False)
            output.seek(0)

            st.download_button(
                label="📥 Download Modified Excel File",
                data=output,
                file_name="modified_file.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Failed to read the Excel file: {e}")
else:
    st.info("Please upload an Excel (.xlsx) file to continue.")
