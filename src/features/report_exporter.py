import json
import os
import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

import features.helper as helper
import features.chat_award as chat_award
import features.roast_mode as roast_mode
import features.reply_speed as reply_speed
import features.ghost_mode as ghost_mode
import features.late_night as late_night
import features.chat_streak as chat_streak
import styles

BASE_CSS_PATH = os.path.join(os.path.dirname(__file__), "..", "css", "base.css")

try:
    with open(BASE_CSS_PATH, "r", encoding="utf-8") as _f:
        _BASE_CSS = _f.read()
except Exception:
    _BASE_CSS = ""


def json_serial(obj):
    """JSON serializer for numpy/pandas scalars."""
    if hasattr(obj, 'item'):
        return obj.item()
    return str(obj)


def _df_to_html_table(dataframe, max_rows=50):
    if dataframe is None or dataframe.empty:
        return ""
    html = dataframe.head(max_rows).to_html(index=False, classes="cr-styled-table")
    return f'<div style="overflow-x:auto;margin-top:12px;margin-bottom:20px;">{html}</div>'


def _generate_wordcloud_html(selected_user, df):
    try:
        df_wc = helper.create_wordcloud_bigrams(selected_user, df)
        if df_wc is not None:
            fig, ax = plt.subplots(figsize=(10, 4.2))
            ax.imshow(df_wc, interpolation="bilinear")
            ax.axis("off")
            fig.patch.set_facecolor("#070B14")
            ax.patch.set_facecolor("#070B14")
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none", dpi=150)
            plt.close(fig)
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode("utf-8")
            return f'<div style="text-align:center;margin:16px 0;"><img src="data:image/png;base64,{img_b64}" style="max-width:100%;border-radius:16px;border:1px solid rgba(255,255,255,0.08);" /></div>'
    except Exception:
        pass
    return ""


# HTML Component Renderers matching styles.py exactly
def _html_chapter_divider(number, title):
    return f"""
<div class="cr-chapter-divider">
    <div class="cr-chapter-num">CHAPTER {number}</div>
    <div class="cr-chapter-title">{title}</div>
    <div class="cr-chapter-line"></div>
</div>"""


def _html_section_header(icon, title, subtitle=""):
    return f"""
<div class="cr-section-header">
    <div class="cr-section-icon">{icon}</div>
    <h2 class="cr-section-title">{title}</h2>
    <p class="cr-section-subtitle">{subtitle}</p>
</div>"""


def _html_metric_card(label, value, subtitle="", icon="📊", color="#8B5CF6"):
    return f"""
<div class="cr-metric-card" style="--accent:{color}">
    <div class="cr-metric-icon">{icon}</div>
    <div class="cr-metric-label">{label}</div>
    <div class="cr-metric-value">{value}</div>
    <div class="cr-metric-sub">{subtitle}</div>
</div>"""


def _html_award_card(icon, title, winner, stat, description=""):
    return f"""
<div class="cr-award-card">
    <div class="cr-award-badge">{icon}</div>
    <div class="cr-award-title">{title}</div>
    <div class="cr-award-winner">{winner}</div>
    <div class="cr-award-stat">{stat}</div>
    <div class="cr-award-desc">{description}</div>
</div>"""


def _html_roast_card(icon, title, winner, stat, roast_text, color="#EC4899"):
    return f"""
<div class="cr-roast-card" style="--accent:{color}">
    <div class="cr-roast-header">
        <span class="cr-roast-icon">{icon}</span>
        <span class="cr-roast-title">{title}</span>
    </div>
    <div class="cr-roast-winner">{winner}</div>
    <div class="cr-roast-stat">{stat}</div>
    <div class="cr-roast-text">"{roast_text}"</div>
</div>"""


def _html_ghost_card(icon, title, suspect, avg_time, evidence_lines=None, color="#06B6D4"):
    evidence_html = ""
    if evidence_lines:
        items = "".join(f'<div class="cr-ghost-evidence-line">{l}</div>' for l in evidence_lines[:4])
        evidence_html = f'<div class="cr-ghost-evidence">{items}</div>'
    return f"""
<div class="cr-ghost-card" style="--accent:{color}">
    <div class="cr-ghost-badge">{icon}</div>
    <div class="cr-ghost-title">{title}</div>
    <div class="cr-ghost-suspect">{suspect}</div>
    <div class="cr-ghost-time">{avg_time}</div>
    {evidence_html}
</div>"""


def _html_sleep_card(icon, label, name, stat, verdict="", color="#8B5CF6"):
    return f"""
<div class="cr-sleep-card" style="--accent:{color}">
    <div class="cr-sleep-icon">{icon}</div>
    <div class="cr-sleep-label">{label}</div>
    <div class="cr-sleep-name">{name}</div>
    <div class="cr-sleep-stat">{stat}</div>
    <div class="cr-sleep-verdict">{verdict}</div>
</div>"""


@st.cache_data(show_spinner=False)
def generate_json_summary(df, selected_user="All"):
    """Generates a structured JSON string of all report findings."""
    num_messages, num_words, num_urls, num_media = helper.fetch_stats(selected_user, df)
    active_days = df["only_date"].nunique() if selected_user == "All" else df[df["Sender"] == selected_user]["only_date"].nunique()
    
    summary = {
        "overview": {
            "selected_user": selected_user,
            "total_messages": int(num_messages),
            "total_words": int(num_words),
            "total_urls": int(num_urls),
            "total_media": int(num_media),
            "active_days": int(active_days),
            "total_participants": int(df["Sender"].nunique()),
        }
    }

    if selected_user == "All":
        awards_data = chat_award.chat_awards(df)
        summary["awards"] = {k: {"title": v["title"], "winner": v["winner"], "value": v["value"], "suffix": v["suffix"]} for k, v in awards_data.items()}
        
        roasts_data = roast_mode.roast_mode(df)
        if roasts_data:
            summary["roasts"] = {k: {"winner": v["winner"], "value": v["value"], "roast": v["roast"]} for k, v in roasts_data.items()}

        ghost = ghost_mode.ghosting_analysis(df)
        if ghost:
            summary["ghosting"] = {
                "longest_ghoster": ghost["biggest_ghoster"],
                "fastest_replier": ghost["fastest"],
                "most_ignored": ghost["ignored_person"],
                "longest_gap_duration_seconds": ghost["longest"]["ghost_seconds"]
            }

        night = late_night.late_night_analysis(df)
        if night:
            summary["late_night"] = {
                "night_owl": night["night_owl"],
                "night_owl_count": night["night_owl_count"],
                "sleep_hours": night["sleep_hours"],
                "personalities": night["personalities"]
            }

        streak = chat_streak.chat_streak_analysis(df)
        if streak:
            summary["streaks"] = {
                "longest_streak_days": streak["longest_streak"],
                "current_streak_days": streak["current_streak"],
                "biggest_break_days": streak["biggest_break"]
            }

    return json.dumps(summary, indent=2, default=json_serial)


@st.cache_data(show_spinner=False)
def generate_html_report(df, selected_user="All"):
    """Generates a complete 1:1 HTML replica matching styles.py components."""
    
    sections_html = []

    # ──────────────────────────────────────────────────────────────────────────
    # 01. THE OVERVIEW
    # ──────────────────────────────────────────────────────────────────────────
    num_messages, num_words, num_urls, num_media = helper.fetch_stats(selected_user, df)
    
    monthly_df = helper.monthly_timeline(selected_user, df)
    monthly_chart_html = ""
    if not monthly_df.empty:
        monthly_fig = px.line(monthly_df, x="time", y="Message", markers=True, title="Monthly Message Trend", color_discrete_sequence=["#8B5CF6"])
        styles.style_plotly_fig(monthly_fig)
        monthly_fig.update_layout(height=320, margin=dict(l=30, r=30, t=40, b=30))
        monthly_chart_html = monthly_fig.to_html(include_plotlyjs=False, full_html=False)

    daily_timeline = helper.daily_timeline(selected_user, df)
    daily_chart_html = ""
    if not daily_timeline.empty:
        daily_fig = px.line(daily_timeline, x="only_date", y="Message", markers=True, title="Daily Message Trend", color_discrete_sequence=["#EC4899"])
        styles.style_plotly_fig(daily_fig)
        daily_fig.update_layout(height=320, margin=dict(l=30, r=30, t=40, b=30))
        daily_chart_html = daily_fig.to_html(include_plotlyjs=False, full_html=False)

    busy_users_chart_html = ""
    contrib_table_html = ""
    if selected_user == "All":
        top_users, percent_df = helper.most_busy_user(df)
        if not top_users.empty:
            df_top = pd.DataFrame({
                "User": [str(u) for u in top_users.index],
                "Messages": [int(v) for v in top_users.values]
            })
            user_fig = px.bar(df_top, x="User", y="Messages", title="Top Active Users", color_discrete_sequence=["#8B5CF6"])
            styles.style_plotly_fig(user_fig)
            user_fig.update_layout(height=320, margin=dict(l=30, r=30, t=40, b=30))
            busy_users_chart_html = user_fig.to_html(include_plotlyjs=False, full_html=False)
        if not percent_df.empty:
            contrib_table_html = _df_to_html_table(percent_df)

    overview_metrics = f"""
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:24px;">
        {_html_metric_card("Total Messages", f"{num_messages:,}", icon="💬", color="#8B5CF6")}
        {_html_metric_card("Total Words", f"{num_words:,}", icon="📝", color="#EC4899")}
        {_html_metric_card("Media Items", f"{num_media:,}", icon="📷", color="#10B981")}
        {_html_metric_card("Links Shared", f"{num_urls:,}", icon="🔗", color="#3B82F6")}
    </div>"""

    sections_html.append(f"""
    {_html_chapter_divider("01", "The Overview")}
    {_html_section_header("📊", "The Overview", "Core activity stats and message breakdown")}
    {overview_metrics}
    {monthly_chart_html}
    {daily_chart_html}
    {busy_users_chart_html}
    {f'<div style="font-weight:700;color:#8B5CF6;font-size:1.05rem;margin-top:20px;margin-bottom:8px;">📋 Contribution Breakdown</div>{contrib_table_html}' if contrib_table_html else ''}
    """)

    # ──────────────────────────────────────────────────────────────────────────
    # 02. SLANG & CATCHPHRASES
    # ──────────────────────────────────────────────────────────────────────────
    wc_image_html = _generate_wordcloud_html(selected_user, df)
    most_common_df, all_words_df = helper.most_common_words(selected_user, df)
    phrases_chart_html = ""
    if not most_common_df.empty:
        if selected_user == "All":
            phrases_fig = px.bar(most_common_df, x="Count", y="Word", color="Sender", orientation="h", barmode="stack", title="Top 20 Phrases Breakdown by Sender", color_discrete_sequence=px.colors.qualitative.Pastel)
        else:
            phrases_fig = px.bar(most_common_df, x="Count", y="Word", orientation="h", title=f"Top 20 Phrases for {selected_user}", color_discrete_sequence=["#8B5CF6"])
        phrases_fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=350, margin=dict(l=30, r=30, t=40, b=30))
        styles.style_plotly_fig(phrases_fig)
        phrases_chart_html = phrases_fig.to_html(include_plotlyjs=False, full_html=False)
    
    phrases_table_html = _df_to_html_table(all_words_df, max_rows=50) if not all_words_df.empty else ""

    sections_html.append(f"""
    {_html_chapter_divider("02", "Slang & Catchphrases")}
    {_html_section_header("🔤", "Slang & Catchphrases", "The words and phrases that define your conversations")}
    {wc_image_html}
    {phrases_chart_html}
    {f'<div style="font-weight:700;color:#8B5CF6;font-size:1.05rem;margin-top:24px;margin-bottom:8px;">📋 Top 50 Most Common Phrases</div>{phrases_table_html}' if phrases_table_html else ''}
    """)

    # ──────────────────────────────────────────────────────────────────────────
    # 03. EMOJI & VIBE CHECK
    # ──────────────────────────────────────────────────────────────────────────
    emoji_df = helper.emoji_helper(selected_user, df)
    emoji_pie_html = ""
    emoji_table_html = ""
    if not emoji_df.empty:
        emoji_table_html = _df_to_html_table(emoji_df, max_rows=20)
        top_emo = emoji_df.head(10).copy()
        top_emo["Sender_Label"] = top_emo["Sender"] + " (" + top_emo["Emoji"] + ")"
        emo_fig = px.pie(top_emo, values="Count", names="Sender_Label", title="Top 10 Most Used Emojis", hole=0.45, color_discrete_sequence=px.colors.qualitative.Pastel)
        emo_fig.update_traces(textposition="inside", textinfo="percent+label")
        styles.style_plotly_fig(emo_fig)
        emo_fig.update_layout(height=320, margin=dict(l=20, r=20, t=35, b=25))
        emoji_pie_html = emo_fig.to_html(include_plotlyjs=False, full_html=False)

    sections_html.append(f"""
    {_html_chapter_divider("03", "Emoji & Vibe Check")}
    {_html_section_header("🎭", "Emoji & Vibe Check", "Which emojis define your conversations?")}
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px;align-items:start;">
        <div>
            <div style="font-weight:700;color:#8B5CF6;font-size:1.05rem;margin-bottom:8px;">📊 Emoji Count Table</div>
            {emoji_table_html}
        </div>
        <div>{emoji_pie_html}</div>
    </div>
    """)

    # ──────────────────────────────────────────────────────────────────────────
    # 04. WHEN ARE WE ACTIVE?
    # ──────────────────────────────────────────────────────────────────────────
    week_map = helper.week_activity_map(selected_user, df)
    week_fig_html = ""
    if not week_map.empty:
        w_df = pd.DataFrame({"Day": list(week_map.index), "Messages": list(week_map.values)})
        w_fig = px.bar(w_df, x="Day", y="Messages", title="Weekly Activity Map", color_discrete_sequence=["#8B5CF6"])
        styles.style_plotly_fig(w_fig)
        w_fig.update_layout(height=300, margin=dict(l=30, r=30, t=40, b=30))
        week_fig_html = w_fig.to_html(include_plotlyjs=False, full_html=False)

    month_map = helper.month_activity_map(selected_user, df)
    month_fig_html = ""
    if not month_map.empty:
        m_df = pd.DataFrame({"Month": list(month_map.index), "Messages": list(month_map.values)})
        m_fig = px.bar(m_df, x="Month", y="Messages", title="Monthly Activity Map", color_discrete_sequence=["#EC4899"])
        styles.style_plotly_fig(m_fig)
        m_fig.update_layout(height=300, margin=dict(l=30, r=30, t=40, b=30))
        month_fig_html = m_fig.to_html(include_plotlyjs=False, full_html=False)

    sections_html.append(f"""
    {_html_chapter_divider("04", "When Are We Active?")}
    {_html_section_header("📈", "Interaction Timelines", "Engagement patterns across days and months")}
    {week_fig_html}
    {month_fig_html}
    """)

    # ──────────────────────────────────────────────────────────────────────────
    # 05. AWARDS
    # ──────────────────────────────────────────────────────────────────────────
    if selected_user == "All":
        awards_data = chat_award.chat_awards(df)
        if awards_data:
            cards = ""
            for key, item in awards_data.items():
                icon = item['title'].split()[0] if 'title' in item else '🏆'
                clean_title = item['title'].split(" ", 1)[1] if " " in item['title'] else item['title']
                cards += _html_award_card(icon, clean_title, item['winner'], f"{item['value']} {item['suffix']}", item.get('description', ''))
            
            sections_html.append(f"""
            {_html_chapter_divider("05", "Awards")}
            {_html_section_header("🏆", "Group Awards", "Recognition for the group's most notable chat personalities")}
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;">{cards}</div>
            """)

    # ──────────────────────────────────────────────────────────────────────────
    # 06. RESPONSE TIME
    # ──────────────────────────────────────────────────────────────────────────
    if selected_user == "All":
        reply_stats = reply_speed.response_time_analysis(df)
        if reply_stats:
            response_cards_html = f"""
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;">
                {_html_metric_card("Fastest Replier", reply_stats['fastest'], "Lightning-fast responses", icon="⚡", color="#10B981")}
                {_html_metric_card("Longest Ignore", reply_stats['longest_ignore_sender'], reply_speed.format_seconds(reply_stats['longest_ignore']), icon="💀", color="#EF4444")}
                {_html_metric_card("Message Ignored To", reply_stats['longest_ignore_to'], "Target of the longest ignore", icon="🎯", color="#F59E0B")}
            </div>"""

            sections_html.append(f"""
            {_html_chapter_divider("06", "Response Time Analysis")}
            {_html_section_header("⚡", "Who Replies Fastest?", "Average response times ranked and exposed")}
            {response_cards_html}
            """)

    # ──────────────────────────────────────────────────────────────────────────
    # 08. CHAT STREAKS
    # ──────────────────────────────────────────────────────────────────────────
    if selected_user == "All":
        streak_data = chat_streak.chat_streak_analysis(df)
        if streak_data:
            days = streak_data["longest_streak"]
            if days >= 365:
                badge, color, desc = "💍 Basically Married", "#F59E0B", "365+ days? Just merge your bank accounts and move in together."
            elif days >= 100:
                badge, color, desc = "❤️ Mutual Obsession", "#EF4444", "Triple digits! Someone is definitely checking their phone every 5 seconds."
            elif days >= 30:
                badge, color, desc = "🔥 Heavy Chemistry", "#10B981", "A whole month straight? The tension is real."
            elif days >= 10:
                badge, color, desc = "😏 Separation Anxiety", "#3B82F6", "The polite, boring phase is officially dead."
            elif days >= 5:
                badge, color, desc = "🌱 Dangerous Spark", "#94a3b8", "Five days running! There is a little fire cooking here."
            else:
                badge, color, desc = "🪦 Ghosted?", "#6B7280", "Radio silence. Did someone get left on read?"

            streak_fig_html = ""
            if "streak_df" in streak_data and not streak_data["streak_df"].empty:
                s_fig = px.line(streak_data["streak_df"], x="date", y="streak", markers=True, title="Chat Streak History", color_discrete_sequence=["#F59E0B"])
                styles.style_plotly_fig(s_fig)
                s_fig.update_layout(height=300, margin=dict(l=30, r=30, t=40, b=30))
                streak_fig_html = s_fig.to_html(include_plotlyjs=False, full_html=False)

            sections_html.append(f"""
            {_html_chapter_divider("08", "Chat Streaks")}
            {_html_section_header("🔥", "Chat Streaks", "Longest daily interaction streaks and milestones")}
            {streak_fig_html}
            <div class="cr-metric-card" style="--accent:{color};display:flex;align-items:center;gap:20px;padding:24px 32px;margin-top:16px;">
                <span style="font-size:48px;">{badge.split()[0]}</span>
                <div>
                    <div style="font-size:11px;font-weight:800;letter-spacing:.15em;text-transform:uppercase;color:{color};margin-bottom:6px;">PEAK STREAK RECORD</div>
                    <div style="font-size:24px;font-weight:900;color:#f1f5f9;margin-bottom:4px;">{badge}</div>
                    <div style="font-size:14px;color:#94a3b8;font-style:italic;">{desc}</div>
                </div>
            </div>
            """)

    # ──────────────────────────────────────────────────────────────────────────
    # 09. CHAT REPORT
    # ──────────────────────────────────────────────────────────────────────────
    if selected_user == "All":
        roasts_data = roast_mode.roast_mode(df)
        if roasts_data:
            cards = ""
            roast_colors = ["#EC4899", "#EF4444", "#F59E0B", "#8B5CF6", "#06B6D4", "#10B981"]
            for idx, (title, item) in enumerate(roasts_data.items()):
                c = roast_colors[idx % len(roast_colors)]
                cards += _html_roast_card("📋", title, item['winner'], f"Value: {item['value']}", item['roast'], color=c)

            sections_html.append(f"""
            {_html_chapter_divider("09", "Chat Report")}
            {_html_section_header("📋", "Chat Report", "Character report based on each member's real chat behaviour")}
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px;">{cards}</div>
            """)

    # ──────────────────────────────────────────────────────────────────────────
    # 10. GHOSTING ANALYSIS
    # ──────────────────────────────────────────────────────────────────────────
    if selected_user == "All":
        ghost = ghost_mode.ghosting_analysis(df)
        if ghost:
            ex = ghost.get("biggest_example", {})
            evidence = []
            if ex:
                evidence = [
                    "🚨 Wanted for emotional neglect.",
                    f'💬 {ex.get("prev_sender", "")}: "{str(ex.get("prev_message", ""))[:30]}..."',
                    f'↩️ {ex.get("reply_sender", "")}: "{str(ex.get("reply_message", ""))[:30]}..."',
                ]
            g1 = _html_ghost_card("👻", "BIGGEST GHOSTER", ghost['biggest_ghoster'], f"Vanishing gap: {ghost_mode.format_ghost_time(ghost['biggest_ghoster_time'])}", evidence, "#EF4444")
            g2 = _html_ghost_card("⚡", "FASTEST REPLIER", ghost['fastest'], "Lightning responder", color="#10B981")
            g3 = _html_ghost_card("🪦", "MOST IGNORED", ghost['ignored_person'], "Left on read pioneer", color="#F59E0B")

            sections_html.append(f"""
            {_html_chapter_divider("10", "Ghosting Analysis")}
            {_html_section_header("👻", "The Disappearance Files", "Detective-grade investigation into vanishing acts and unreplied texts")}
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;">
                {g1}{g2}{g3}
            </div>
            """)

    # ──────────────────────────────────────────────────────────────────────────
    # 11. SLEEP DEPRIVATION
    # ──────────────────────────────────────────────────────────────────────────
    if selected_user == "All":
        night = late_night.late_night_analysis(df)
        if night:
            s1 = _html_sleep_card("🧛‍♂️", "THE VAMPIRE", night['night_owl'], f"{night['night_owl_count']} texts after midnight", "Literally has not seen the sun in years.", "#8B5CF6")
            s2 = _html_sleep_card("🛌", "RESPONSIBLE ADULT", night['best_sleeper'], f"{night['best_score']}% day activity", "Probably drinks 8 glasses of water.", "#10B981")
            s3 = _html_sleep_card("🧟", "INSOMNIAC PRIME", night['worst_sleeper'], f"{night['worst_score']}% night ratio", "Powered purely by anxiety.", "#EF4444")
            s4 = _html_sleep_card("😈", "THE DEMON HOUR", f"{night['demon_hour']}:00", f"{night['demon_count']} texts of pure chaos", "When brain cells die.", "#EC4899")

            sections_html.append(f"""
            {_html_chapter_divider("11", "The Insomnia Chronicles")}
            {_html_section_header("🌙", "Who Needs Sleep When You Have WiFi?", "A brutal exposure of your group's circadian rhythm violations")}
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;">
                {s1}{s2}{s3}{s4}
            </div>
            """)

    all_content = "\n".join(sections_html)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Rewind Report — {selected_user}</title>
    <!-- Load Plotly JS once in head to prevent empty void charts -->
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <style>
        body {{
            background-color: #070B14;
            color: #f8fafc;
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}
        .app-wrapper {{
            max-width: 1000px;
            width: 100%;
        }}
        .cr-styled-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 0.9rem;
        }}
        .cr-styled-table th {{
            background: rgba(139, 92, 246, 0.15);
            color: #c4b5fd;
            text-align: left;
            padding: 10px 14px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .cr-styled-table td {{
            padding: 10px 14px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            color: #e2e8f0;
        }}
        .cr-styled-table tr:hover {{
            background: rgba(255,255,255,0.03);
        }}
        {_BASE_CSS}
    </style>
</head>
<body>
    <div class="app-wrapper">
        <!-- TOP BANNER -->
        <div class="cr-topbar" style="margin-bottom:32px;">
            <div class="cr-topbar-brand">
                <span class="cr-topbar-logo">💬</span>
                <span class="cr-topbar-name">CHAT REWIND</span>
            </div>
            <div class="cr-topbar-tagline">Complete 1:1 Visual Export — Filter: <strong>{selected_user}</strong></div>
        </div>

        {all_content}

        <!-- FOOTER -->
        <div class="cr-chapter-divider" style="margin-top:40px;">
            <div class="cr-chapter-line"></div>
        </div>
        <div class="cr-footer">
            <div class="cr-footer-brand">💬 Chat Rewind</div>
            <div class="cr-footer-copy">Exported report from WhatsApp Chat Rewind Analysis</div>
        </div>
    </div>
</body>
</html>
"""
    return full_html
