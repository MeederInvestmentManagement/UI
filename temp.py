# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18

@author: jdevore
"""

import streamlit as st
import pandas as pd
from Calculator import add_two_to_numbers
from io import BytesIO # for creating a file in memory
import re  # for cleaning the option name for filenames

st.set_page_config(layout="wide", page_title="Excel A1 Reader & Calculator")

# Main title
st.markdown("## 📁 Please upload an Excel file")

# File uploader (main area)
uploaded_file = st.file_uploader(
    "### Drag and drop or browse to upload (.xlsx only)", type=["xlsx"]
)

# Dropdown menu for actions
option = st.selectbox(
    "Choose an action to perform:",
    ("Read cell A1", "Preview sheet", "Show entire file", "Add 2 to all numbers"),
    index=0
)

# Excel file handling
if uploaded_file:
    try:
        # Read uploaded Excel file
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

            # Create downloadable Excel file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                modified_df.to_excel(writer, index=False, header=False)
            output.seek(0)

            # Create a clean filename based on upload and action
            base_filename = uploaded_file.name.rsplit('.', 1)[0]
            clean_option = re.sub(r'\W+', '_', option.strip())
            final_filename = f"{base_filename}_{clean_option}.xlsx"

            # Download button
            st.download_button(
                label="📥 Download Modified Excel File",
                data=output,
                file_name=final_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Failed to read the Excel file: {e}")
else:
    st.info("Please upload an Excel (.xlsx) file to continue.")
