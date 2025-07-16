import streamlit as st
from PIL import Image
from components import dashboard, form, full_table

st.set_page_config(layout="wide", page_title="RAAP", initial_sidebar_state="collapsed")


# === ROW: Logo (left), Spacer (middle), Nav (right) ===
col1, col2, col3 = st.columns([1, 4, 2])

with col1:
    logo = Image.open("assets/logo.png")
    st.image(logo, width=250)

with col3:
    st.markdown("<div style='text-align: right; padding-top: 1.2rem;'>", unsafe_allow_html=True)
    nav = st.radio(
        "",
        options=["Dashboard", "Form + Table", "Full Table"],
        horizontal=True,
        label_visibility="collapsed",
        key="nav_bar"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# === PAGE ROUTING ===
if nav == "Dashboard":
    dashboard.show_dashboard()
elif nav == "Form + Table":
    form.show_form_table()
elif nav == "Full Table":
    full_table.show_full_table()
