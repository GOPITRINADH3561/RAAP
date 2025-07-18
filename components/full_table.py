# components/full_table.py

import streamlit as st
import pandas as pd
import os

DATA_PATH = "data/tracker_data.csv"

def show_full_table():
    st.subheader("📊 Full Table View with Customization")

    if not os.path.exists(DATA_PATH):
        st.warning("No data available.")
        return

    df = pd.read_csv(DATA_PATH)

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

    # Option to download data
    csv = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Table as CSV",
        data=csv,
        file_name="RAAP_Tracker_Export.csv",
        mime="text/csv",
    )

    # Save changes if any
    if edited_df.equals(df) == False:
        st.success("✅ Changes updated successfully.")
        edited_df.to_csv(DATA_PATH, index=False)
