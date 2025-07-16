import streamlit as st
import pandas as pd
import plotly.express as px
import os

DATA_PATH = "data/tracker_data.csv"

def load_data(path):
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except Exception:
            return pd.DataFrame(columns=["Professor Name", "Professor Mail", "Department", "FollowUp"])
    return pd.DataFrame(columns=["Professor Name", "Professor Mail", "Department", "FollowUp"])

def styled_card(metric: str, label: str, color: str = "#f0f2f6"):
    st.markdown(f"""
    <div style="
        padding: 1.5rem;
        border-radius: 1.25rem;
        background: {color};
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        text-align: center;
        font-weight: 600;
        font-size: 1.4rem;
        color: #1f2937;">
        <div style="font-size: 2.2rem; font-weight: bold;">{metric}</div>
        <div style="margin-top: 0.5rem;">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def show_dashboard():
    st.title("📊 Assistantship Tracker Dashboard")

    df = load_data(DATA_PATH)

    if df.empty:
        st.warning("No data available to display.")
        return

    # Counters
    total_apps = len(df)
    pending_followups = df["FollowUp"].sum() if "FollowUp" in df.columns else 0
    departments = df["Department"].nunique()

    st.markdown("### 📌 Summary")
    c1, c2, c3 = st.columns(3)
    with c1:
        styled_card(total_apps, "Total Applications", "#e3f2fd")
    with c2:
        styled_card(int(pending_followups), "Pending Follow-Ups", "#fff3e0")
    with c3:
        styled_card(departments, "Departments Contacted", "#ede7f6")

    st.markdown("---")

    # Applications by Department
    st.markdown("### 🗂️ Applications by Department")
    dept_counts = df["Department"].value_counts().reset_index()
    dept_counts.columns = ["Department", "Count"]

    fig_bar = px.bar(
        dept_counts,
        x="Department",
        y="Count",
        color="Department",
        title="Applications per Department",
        template="plotly_white"
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

    # Follow-up status
    st.markdown("### 🔁 Follow-Up Analysis")
    if "FollowUp" in df.columns:
        followup_data = df["FollowUp"].value_counts().rename(index={0: "Not Needed", 1: "Needed"}).reset_index()
        followup_data.columns = ["Status", "Count"]

        col1, col2 = st.columns(2)

        with col1:
            fig_donut = px.pie(
                followup_data,
                names="Status",
                values="Count",
                hole=0.55,
                title="Follow-Up Breakdown",
                color_discrete_sequence=["#81d4fa", "#ffab91"]
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        with col2:
            fig_box = px.box(
                df,
                x="Department",
                y="FollowUp",
                title="Follow-Up Requests by Department",
                color="Department",
                points="all",
                template="plotly_white"
            )
            st.plotly_chart(fig_box, use_container_width=True)
