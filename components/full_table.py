# components/full_table.py

import streamlit as st
import pandas as pd
from utils.helpers import load_data, save_data, ensure_data_file

DATA_PATH = "data/tracker_data.csv"

def show_full_table():
    st.subheader("📋 Full Table View with Customization")

    ensure_data_file(DATA_PATH)  # ✅ make sure file exists with correct columns
    df = load_data(DATA_PATH)

    if df.empty:
        st.info("No entries yet.")
        return

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="full_table_editor"
    )

    # Save changes if any
    if not edited_df.equals(df):
        save_data(edited_df, DATA_PATH)
        st.success("✅ Changes updated successfully.")

    # Download button
    csv = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Table as CSV",
        data=csv,
        file_name="RAAP_Tracker_Export.csv",
        mime="text/csv",
    )
