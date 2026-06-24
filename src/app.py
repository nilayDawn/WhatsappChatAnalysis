import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

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

        # Finding busiest users in the group (Group Level)
        if selected_user == "All":
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color="orange")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Frequently Used Words")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)

        if not most_common_df.empty:
            if selected_user == 'All':
                # Create a stacked bar chart showing contributions from each sender
                fig = px.bar(
                    most_common_df,
                    x="Count",
                    y="Word",
                    color="Sender",       # This splits the bar into colors based on the sender
                    orientation="h",
                    barmode="stack",
                    title="Top 20 Words Breakdown by Sender"
                )
            else:
                # Standard solid-color bar chart for a single user
                fig = px.bar(
                    most_common_df,
                    x="Count",
                    y="Word",
                    orientation="h",
                    title=f"Top 20 Words for {selected_user}"
                )

            # Force Plotly to sort the bars so the longest one is at the top
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})

            # Display the interactive chart
            st.plotly_chart(fig, use_container_width=True)
    
        else:
            st.info("No words found. This chat might be empty or entirely media files.")

            
        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            top = emoji_df.head(10)
            top['Sender_Label'] = top['Sender'] + " (" + top['Emoji'] + ")"
            if not top.empty:
                # Create an interactive pie chart using Plotly Express
                fig = px.pie(
                    top, 
                    values='Count', 
                    names='Sender_Label',
                    title='Top 10 Most Common Emojis',
                    hole=0.3 # Optional: makes it a donut chart which often looks cleaner
                )
        
                # Force the labels and percentages to show up directly on the chart
                fig.update_traces(textposition='inside', textinfo='percent+label')
        
                # Display the chart in Streamlit
                st.plotly_chart(fig, use_container_width=True)

