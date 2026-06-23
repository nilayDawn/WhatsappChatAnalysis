import streamlit as st
import pandas as pd

from preprocessing import preprocess



st.set_page_config(layout="wide")
st.sidebar.title("WhatsApp Chat Analyzer")

# 1. File Uploader widget in the UI
uploaded_file = st.file_uploader("Upload your WhatsApp Chat (.txt) file", type=["txt"])

if uploaded_file is not None:
    st.info("Preprocessing chat locally in Streamlit...")

    # Read uploaded file bytes and decode to text
    content = uploaded_file.getvalue()
    text = content.decode("utf-8-sig")

    # Directly call preprocessing instead of sending to FastAPI
    df = preprocess(text)

    st.success("Analysis Complete!")
    st.metric(label="Total Messages Parsed", value=len(df))
    st.dataframe(df)

    # Fetch Unique users
    user_list = df["Sender"].unique().tolist()
    user_list.sort()

    st.sidebar.selectbox(
        "Select a User to Filter Messages",
        options=["All"] + user_list,
        index=0,
        key="user_filter",
    )

    if st.sidebar.button("Show Analysis"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
