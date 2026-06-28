import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from preprocessing import preprocess
import helper
import styles

# Initialize page settings
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS styles
styles.load_css()

# Render custom header UI
styles.render_header()

# Sidebar control panel header
st.sidebar.markdown(
    """
<div style="padding: 10px 0; margin-bottom: 20px;">
    <h2 style="margin: 0; font-size: 1.6rem; font-weight: 800; color: #a5b4fc; display: flex; align-items: center; gap: 8px;">
        ⚡ Control Panel
    </h2>
</div>
""",
    unsafe_allow_html=True,
)


# Cache Preprocessing function to avoid re-running on every interaction
@st.cache_data(show_spinner=False)
def cached_preprocess(text):
    return preprocess(text)


# 1. File Uploader widget in the UI
uploaded_file = st.file_uploader("Upload your WhatsApp Chat (.txt) file", type=["txt"])

if uploaded_file is None:
    # If no file is uploaded, show the gorgeous onboarding guide
    styles.render_instructions()
    st.info(
        "💡 **Awaiting chat upload...** Please select your WhatsApp chat log to begin."
    )
else:
    # Read uploaded file bytes and decode to text
    content = uploaded_file.getvalue()
    text = content.decode("utf-8-sig")

    # Call preprocessing helper
    df = cached_preprocess(text)

    # Success feedback and overall parse statistics
    st.markdown(
        '<div class="section-title">📁 Uploaded Chat Session</div>',
        unsafe_allow_html=True,
    )

    col_stat1, col_stat2 = st.columns([1, 3])
    with col_stat1:
        st.markdown(
            f"""
        <div class="metric-card" style="margin: 0; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div class="metric-icon" style="font-size: 2rem;">📊</div>
            <div class="metric-label" style="font-size: 0.85rem;">Total Messages Parsed</div>
            <div class="metric-value" style="font-size: 2.5rem;">{len(df):,}</div>
            <div class="metric-user">💬 Chat Preprocessing Complete</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col_stat2:
        with st.expander("🔍 View Raw Parsed Dataframe", expanded=False):
            st.dataframe(df, use_container_width=True)

    # Fetch Unique users for select box
    # cache user list
    @st.cache_data(show_spinner=False)
    def get_users(df):
        users = df["Sender"].unique().tolist()
        users.sort()
        return users

    user_list = get_users(df)

    selected_user = st.sidebar.selectbox(
        "Select a User to Filter Messages",
        options=["All"] + user_list,
        index=0,
        key="user_filter",
    )

    st.sidebar.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    if st.sidebar.button("Show Analysis"):
        st.session_state["show_analysis"] = True

    if st.session_state.get("show_analysis", False):
        with st.spinner("⏳ Analyzing chat data..."):
            # Fetch stats
            num_messages, num_words, num_urls, num_media_messages = helper.fetch_stats(
                selected_user, df
            )

            # 4-Column Metric Cards layout
            st.markdown(
                '<div class="section-title">📊 Key Metrics Overview</div>',
                unsafe_allow_html=True,
            )
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                styles.render_metric_card(
                    "Total Messages", f"{num_messages:,}", selected_user, icon="✉️"
                )
            with col2:
                styles.render_metric_card(
                    "Total Words", f"{num_words:,}", selected_user, icon="📝"
                )
            with col3:
                styles.render_metric_card(
                    "Media Omitted", f"{num_media_messages:,}", selected_user, icon="🖼️"
                )
            with col4:
                styles.render_metric_card(
                    "Links Shared", f"{num_urls:,}", selected_user, icon="🔗"
                )

            # Finding busiest users in the group (Group Level)
            if selected_user == "All":
                st.markdown(
                    '<div class="section-title">👥 User Contribution & Activity</div>',
                    unsafe_allow_html=True,
                )
                x, new_df = helper.most_busy_user(df)

                col_busy1, col_busy2 = st.columns([3, 2])
                with col_busy1:
                    # Create a beautiful interactive Plotly bar chart
                    fig = px.bar(
                        x=x.index,
                        y=x.values,
                        labels={"x": "User", "y": "Number of Messages"},
                        title="Top 5 Most Active Users",
                        color=x.values,
                        color_continuous_scale="Purples",
                    )
                    fig.update_layout(coloraxis_showscale=False)
                    styles.style_plotly_fig(fig)
                    st.plotly_chart(fig, use_container_width=True)
                with col_busy2:
                    st.markdown(
                        "<div style='padding-top: 10px; font-weight:600; color:#a5b4fc; font-size:1.1rem; margin-bottom:8px;'>Percentage Contribution</div>",
                        unsafe_allow_html=True,
                    )
                    st.dataframe(new_df, use_container_width=True)

        # WordCloud and Common Words section using Tabs
        st.markdown(
            '<div class="section-title">🔤 Vocabulary & Phrase Analysis</div>',
            unsafe_allow_html=True,
        )

        most_common_df, all_words_df = helper.most_common_words(selected_user, df)
        tab_wc, tab_words = st.tabs(["✨ Word Cloud", "📊 Most Common Words"])

        with tab_wc:
            df_wc = helper.create_wordcloud_bigrams(selected_user, df)
            if df_wc is not None:
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(df_wc, interpolation="bilinear")
                ax.axis("off")
                fig.patch.set_facecolor("none")  # Make background transparent
                ax.patch.set_facecolor("none")
                st.pyplot(fig, clear_figure=True)
                plt.close(fig)  # Close the figure to free memory
            else:
                st.info(
                    "No words found. This chat might be empty or entirely media files."
                )

        with tab_words:
            if not most_common_df.empty:
                if selected_user == "All":
                    # Create a stacked bar chart showing contributions from each sender
                    fig = px.bar(
                        most_common_df,
                        x="Count",
                        y="Word",
                        color="Sender",
                        orientation="h",
                        barmode="stack",
                        title="Top 20 Words Breakdown by Sender",
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                    )
                else:
                    # Standard solid-color bar chart for a single user
                    fig = px.bar(
                        most_common_df,
                        x="Count",
                        y="Word",
                        orientation="h",
                        title=f"Top 20 Words for {selected_user}",
                        color_discrete_sequence=["#818cf8"],
                    )

                # Force Plotly to sort the bars so the longest one is at the top
                fig.update_layout(yaxis={"categoryorder": "total ascending"})
                styles.style_plotly_fig(fig)

                # Display the interactive chart
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(
                    "No words found. This chat might be empty or entirely media files."
                )

        # Display the dataframe (always visible below the tabs)
        if not all_words_df.empty:
            st.markdown(
                "<div style='font-weight:600; color:#a5b4fc; font-size:1.1rem; margin-top:20px; margin-bottom:8px;'>Top 50 Most Common Phrases Data</div>",
                unsafe_allow_html=True,
            )
            st.dataframe(all_words_df, use_container_width=True)

        # Emoji analysis section
        st.markdown(
            '<div class="section-title">🎭 Sentiment & Emoji Analysis</div>',
            unsafe_allow_html=True,
        )
        emoji_df = helper.emoji_helper(selected_user, df)

        if not emoji_df.empty:
            col_emo1, col_emo2 = st.columns([2, 3])
            with col_emo1:
                st.markdown(
                    "<div style='font-weight:600; color:#a5b4fc; font-size:1.1rem; margin-bottom:8px;'>Emoji Count Table</div>",
                    unsafe_allow_html=True,
                )
                st.dataframe(emoji_df, use_container_width=True)
            with col_emo2:
                top = emoji_df.head(10).copy()
                top["Sender_Label"] = top["Sender"] + " (" + top["Emoji"] + ")"
                if not top.empty:
                    # Create an interactive pie/donut chart using Plotly Express
                    fig = px.pie(
                        top,
                        values="Count",
                        names="Sender_Label",
                        title="Top 10 Most Common Emojis",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                    )

                    # Force the labels and percentages to show up directly on the chart
                    fig.update_traces(textposition="inside", textinfo="percent+label")
                    styles.style_plotly_fig(fig)

                    # Display the chart in Streamlit
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No emojis found.")
        else:
            st.info(
                "No emojis found. This chat might be empty or entirely media files."
            )

        # Timelines section using Tabs
        st.markdown(
            '<div class="section-title">📈 Interaction Timelines</div>',
            unsafe_allow_html=True,
        )
        tab_monthly, tab_daily = st.tabs(["📅 Monthly Timeline", "📈 Daily Timeline"])

        with tab_monthly:
            timeline = helper.monthly_timeline(selected_user, df)
            if not timeline.empty:
                monthly_fig = px.line(
                    timeline,
                    x="time",
                    y="Message",
                    markers=True,
                    title="Messages per Month",
                    labels={"time": "Month", "Message": "Messages"},
                    color_discrete_sequence=["#818cf8"],
                )
                monthly_fig.update_layout(xaxis_tickangle=-45)
                styles.style_plotly_fig(monthly_fig)
                st.plotly_chart(monthly_fig, use_container_width=True)
            else:
                st.info("No timeline data available.")

        with tab_daily:
            daily_timeline = helper.daily_timeline(selected_user, df)
            if not daily_timeline.empty:
                daily_fig = px.line(
                    daily_timeline,
                    x="only_date",
                    y="Message",
                    markers=True,
                    title="Messages per Day",
                    labels={"only_date": "Date", "Message": "Messages"},
                    color_discrete_sequence=["#a78bfa"],
                )
                daily_fig.update_layout(xaxis_tickangle=-45)
                styles.style_plotly_fig(daily_fig)
                st.plotly_chart(daily_fig, use_container_width=True)
            else:
                st.info("No daily data available.")

        # Activity maps section using Tabs
        st.markdown(
            '<div class="section-title">⏱️ Activity & Engagement Patterns</div>',
            unsafe_allow_html=True,
        )
        tab_days, tab_months, tab_heatmap = st.tabs(
            ["📆 Weekly Activity Map", "🗓️ Monthly Activity Map", "🔥 Hourly Heatmap"]
        )

        with tab_days:
            busy_day = helper.week_activity_map(selected_user, df)
            if busy_day is not None and len(busy_day) > 0:
                busy_day_df = busy_day.reset_index()
                busy_day_df.columns = ["day_name", "Message"]
                busy_day_df["day_name"] = pd.Categorical(
                    busy_day_df["day_name"],
                    categories=[
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thursday",
                        "Friday",
                        "Saturday",
                        "Sunday",
                    ],
                    ordered=True,
                )
                busy_day_df = busy_day_df.sort_values("day_name")
                busy_day_df["Message"] = pd.to_numeric(
                    busy_day_df["Message"], errors="coerce"
                ).fillna(0)

                busy_day_fig = px.bar(
                    busy_day_df,
                    x="day_name",
                    y="Message",
                    title="Messages by Day of Week",
                    labels={"day_name": "Day", "Message": "Messages"},
                    color="Message",
                    color_continuous_scale="Sunsetdark",
                )
                busy_day_fig.update_layout(
                    coloraxis_showscale=False, xaxis_tickangle=-45
                )
                styles.style_plotly_fig(busy_day_fig)
                st.plotly_chart(busy_day_fig, use_container_width=True)
            else:
                st.info("No day activity data available.")

        with tab_months:
            busy_month = helper.month_activity_map(selected_user, df)
            if busy_month is not None and len(busy_month) > 0:
                busy_month_df = busy_month.reset_index()
                busy_month_df.columns = ["month", "Message"]
                month_order = [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ]
                busy_month_df["month"] = pd.Categorical(
                    busy_month_df["month"],
                    categories=month_order,
                    ordered=True,
                )
                busy_month_df = busy_month_df.sort_values("month")
                busy_month_df["Message"] = pd.to_numeric(
                    busy_month_df["Message"], errors="coerce"
                ).fillna(0)

                busy_month_fig = px.bar(
                    busy_month_df,
                    x="month",
                    y="Message",
                    title="Messages by Month",
                    labels={"month": "Month", "Message": "Messages"},
                    color="Message",
                    color_continuous_scale="Sunsetdark",
                )
                busy_month_fig.update_layout(
                    coloraxis_showscale=False, xaxis_tickangle=-45
                )
                styles.style_plotly_fig(busy_month_fig)
                st.plotly_chart(busy_month_fig, use_container_width=True)
            else:
                st.info("No month activity data available.")

        with tab_heatmap:
            user_heatmap = helper.activity_heatmap(selected_user, df)
            if user_heatmap is not None and not user_heatmap.empty:
                heatmap_fig = px.imshow(
                    user_heatmap,
                    aspect="auto",
                    color_continuous_scale="Viridis",
                    labels={
                        "x": "Period (hour ranges)",
                        "y": "Day",
                        "color": "Messages",
                    },
                    title="Messages Heatmap (Day vs Time Period)",
                )
                styles.style_plotly_fig(heatmap_fig)
                st.plotly_chart(heatmap_fig, use_container_width=True)
            else:
                st.info("No weekly heatmap data available.")
