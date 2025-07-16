import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd

def render_table(df, path):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=False, filter=True, sortable=True, resizable=True)

    # FollowUp column with editable checkbox
    gb.configure_column(
        "FollowUp",
        editable=True,
        cellEditor='agCheckboxCellEditor',
        cellStyle={"justifyContent": "center"}
    )

    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=6)
    gb.configure_grid_options(domLayout='normal')

    # Apply dark theme and smooth corners
    st.markdown("""
        <style>
        .ag-theme-streamlit {
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            background-color: #1e1e1e;
            padding: 0.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .ag-header-cell-label {
            font-weight: 600;
            color: #f1f1f1;
        }
        .ag-row {
            font-size: 15px;
            color: #e0e0e0;
            background-color: #202020;
        }
        .ag-row:hover {
            background-color: #2a2a2a !important;
        }
        </style>
    """, unsafe_allow_html=True)

    grid_return = AgGrid(
        df,
        gridOptions=gb.build(),
        height=420,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        theme="streamlit"
    )

    updated_df = grid_return["data"]
    updated_df.to_csv(path, index=False)
