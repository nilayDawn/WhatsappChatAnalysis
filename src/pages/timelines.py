import streamlit as st
import pandas as pd
import plotly.express as px
import helper
import styles


def render(selected_user, df):
    """Renders the Timelines & Activity Patterns page."""

    # ── Interaction Timelines ─────────────────────────────────────────────────
    styles.render_section_header("📈", "Interaction Timelines",
                                 "How your conversations evolved over time")

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
                color_discrete_sequence=["#8B5CF6"],
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
                color_discrete_sequence=["#EC4899"],
            )
            daily_fig.update_layout(xaxis_tickangle=-45)
            styles.style_plotly_fig(daily_fig)
            st.plotly_chart(daily_fig, use_container_width=True)
        else:
            st.info("No daily data available.")

    # ── Activity Patterns ─────────────────────────────────────────────────────
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    styles.render_section_header("⏱️", "Activity & Engagement Patterns",
                                 "When does your group come alive?")

    tab_days, tab_months, tab_heatmap = st.tabs(
        ["📆 Weekly Activity", "🗓️ Monthly Activity", "🔥 Hourly Heatmap"]
    )

    with tab_days:
        busy_day = helper.week_activity_map(selected_user, df)
        if busy_day is not None and len(busy_day) > 0:
            busy_day_df = busy_day.reset_index()
            busy_day_df.columns = ["day_name", "Message"]
            busy_day_df["day_name"] = pd.Categorical(
                busy_day_df["day_name"],
                categories=[
                    "Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday",
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
                color_continuous_scale=["#1e1b4b", "#8B5CF6", "#EC4899"],
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
                "January", "February", "March", "April",
                "May", "June", "July", "August",
                "September", "October", "November", "December",
            ]
            busy_month_df["month"] = pd.Categorical(
                busy_month_df["month"], categories=month_order, ordered=True
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
                color_continuous_scale=["#1e1b4b", "#3B82F6", "#8B5CF6"],
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
                color_continuous_scale=["#070B14", "#1e1b4b", "#8B5CF6", "#EC4899"],
                labels={"x": "Period (hour ranges)", "y": "Day", "color": "Messages"},
                title="Messages Heatmap (Day vs Time Period)",
            )

            #Force Plotly to treat axes as categorical strings
            heatmap_fig.update_xaxes(type='category')
            heatmap_fig.update_yaxes(type='category')

            styles.style_plotly_fig(heatmap_fig)
            st.plotly_chart(heatmap_fig, use_container_width=True)
        else:
            st.info("No weekly heatmap data available.")
