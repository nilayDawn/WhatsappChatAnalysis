import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from preprocessing import preprocess
import helper


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

    selected_user = st.sidebar.selectbox(
        "Select a User to Filter Messages",
        options=["All"] + user_list,
        index=0,
        key="user_filter",
    )

    if st.sidebar.button("Show Analysis"):

        num_messages, num_words, num_urls, num_media_messages = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.subheader(f"{selected_user}")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.subheader(f"{selected_user}")
            st.title(num_words)
        with col3:
            st.header("Total Media Messages")
            st.subheader(f"{selected_user}")
            st.title(num_media_messages)
        with col4:
            st.header("Total Links Shared")
            st.subheader(f"{selected_user}")
            st.title(num_urls)

        #Finding busiest users in the group(Group Level)
        if selected_user == 'All':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title("Frequently Used Words")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)