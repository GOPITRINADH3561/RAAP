from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
import streamlit as st
import pandas as pd
import os
from utils.helpers import sanitize_email, ensure_data_file, load_data, save_data, add_entry, delete_entry



# --- Constants ---
DATA_PATH = "data/tracker_data.csv"
DEPARTMENTS = ["Computer Science", "Electrical and Computer Engineering", "Mechanical Engineering", "Civil Engineering", "Biomedical Engineering", "Chemical Engineering", "Industrial Engineering", "Materials Science and Engineering", "Physics", "Mathematics", "Statistics", "Data Science", "Environmental Engineering", "Petroleum Engineering", "Systems Engineering", "Information Science", "Computational Science", "Aerospace Engineering", "Robotics", "Artificial Intelligence", "Psychology", "Cognitive Science", "Business Analytics", "Finance", "Economics", "Management Information Systems", "Education", "Public Health", "Health Informatics", "Digital Media", "Architecture", "Design", "Urban Planning", "Earth and Atmospheric Sciences", "Chemistry", "Biology", "Biotechnology", "Others"
]

# --- Utils ---
def sanitize_email(raw_email):
    return raw_email.strip().split("@")[0] + "@uh.edu"

def load_data(path):
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            if "FollowUp" not in df.columns:
                df["FollowUp"] = False
            return df
        except Exception:
            pass
    return pd.DataFrame(columns=["Professor Name", "Professor Mail", "Department", "FollowUp"])

def save_data(df, path):
    df.to_csv(path, index=False)

def add_entry(name, email, department):
    df = load_data(DATA_PATH)
    clean_email = sanitize_email(email)
    if ((df["Professor Name"] == name) & (df["Professor Mail"] == clean_email)).any():
        st.warning("🚫 This professor already exists.")
        return
    new_entry = {
        "Professor Name": name,
        "Professor Mail": clean_email,
        "Department": department,
        "FollowUp": False
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    save_data(df, DATA_PATH)
    st.success("✅ Entry added.")

def delete_entry(name, email):
    df = load_data(DATA_PATH)
    clean_email = sanitize_email(email)
    initial_len = len(df)
    df = df[~((df["Professor Name"] == name) & (df["Professor Mail"] == clean_email))]
    if len(df) < initial_len:
        save_data(df, DATA_PATH)
        st.success("🗑️ Entry deleted.")
    else:
        st.error("❌ No matching entry found to delete.")

def show_table_with_features(df: pd.DataFrame):
    # JS to highlight the entire row when FollowUp is true
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
    gb.configure_column("FollowUp", editable=True)
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


# --- Main UI ---
def show_form_table():
    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container(border=True):
            st.subheader("✍️ Professor Application")

            with st.expander("📁 Setup Tracker File", expanded=False):
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
                        add_entry(name.strip(), email.strip(), department)

                if delete:
                    if not name.strip() or not email.strip():
                        st.warning("⚠️ Provide name and email to delete.")
                    else:
                        delete_entry(name.strip(), email.strip())

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
