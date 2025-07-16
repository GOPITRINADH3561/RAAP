# components/form.py

import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

from utils.helpers import sanitize_email, ensure_data_file, load_data, save_data, add_entry, delete_entry

DATA_PATH = "data/tracker_data.csv"
DEPARTMENTS = ["ECE", "CSE", "ME", "CE", "Others"]

# -- File Upload or Create UI --
def handle_data_file_ui():
    st.subheader("📁 Setup Tracker File")

    option = st.radio("Select Data Mode", ["Upload Existing CSV", "Create New Tracker File"], horizontal=True)

    if option == "Upload Existing CSV":
        uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
        if uploaded_file is not None:
            try:
                df_uploaded = pd.read_csv(uploaded_file)
                st.success("✅ File uploaded successfully. Preview:")
                st.dataframe(df_uploaded, use_container_width=True)

                if st.button("📥 Save Uploaded File as Tracker"):
                    os.makedirs("data", exist_ok=True)
                    save_data(df_uploaded, DATA_PATH)
                    st.success("💾 Saved as current tracker file.")
            except Exception as e:
                st.error(f"❌ Error reading CSV: {e}")
        else:
            st.info("Please upload a CSV file.")

    elif option == "Create New Tracker File":
        if not os.path.exists(DATA_PATH):
            ensure_data_file(DATA_PATH)
            st.success("🆕 New tracker file created.")
        else:
            st.info("📁 Tracker file already exists.")


# -- AgGrid Table Styling --
def show_table_with_features(df: pd.DataFrame):
    row_style = JsCode("""
        function(params) {
            if (params.data.FollowUp === true) {
                return {
                    'backgroundColor': '#e6f4ea',
                    'color': '#1a1a1a',
                    'fontWeight': '500',
                    'border': '1px solid #cce3d8'
                }
            }
            return {}
        }
    """)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)
    gb.configure_default_column(filter=True, sortable=True, resizable=True)
    gb.configure_column("FollowUp", editable=True, cellEditor='agCheckboxCellEditor')
    gb.configure_grid_options(getRowStyle=row_style)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        enable_enterprise_modules=False,
        allow_unsafe_jscode=True,
        theme="streamlit",
        fit_columns_on_grid_load=True,
        use_container_width=True
    )

    updated_df = grid_response["data"]
    if not updated_df.equals(df):
        save_data(updated_df, DATA_PATH)

    followup_count = updated_df["FollowUp"].sum()
    st.info(f"🔁 Professors needing follow-up: **{followup_count}**")


# -- Main Page --
def show_form_table():
    handle_data_file_ui()
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container(border=True):
            st.subheader("✍️ Professor Application")

            with st.form("professor_form", clear_on_submit=True):
                name = st.text_input("Professor Name")
                email = st.text_input("Email (any form)")
                department = st.selectbox("Department", DEPARTMENTS)

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    submit = st.form_submit_button("Submit Entry")
                with col_btn2:
                    delete = st.form_submit_button("Delete Entry")

                if submit:
                    if not name.strip() or not email.strip():
                        st.warning("⚠️ All fields must be filled.")
                    else:
                        add_entry(name.strip(), email.strip(), department, DATA_PATH)

                if delete:
                    if not name.strip() or not email.strip():
                        st.warning("⚠️ Provide name and email to delete.")
                    else:
                        delete_entry(name.strip(), email.strip(), DATA_PATH)

    with col2:
        st.subheader("📁 Existing Applications")
        df = load_data(DATA_PATH)
        if df.empty:
            st.info("No entries found.")
        else:
            show_table_with_features(df)


if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    show_form_table()
