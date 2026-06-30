import streamlit as st
import features.ghost_mode as ghost_mode
import styles

def render(df):
    """Chapter 7: Ghosting Analysis — Detective case files."""

    styles.render_chapter_divider("07", "Ghosting Analysis")

    styles.render_section_header(
        "👻", 
        "The Disappearance Files",
        "Detective-grade investigation into every vanishing act and unreplied text."
    )

    ghost = ghost_mode.ghosting_analysis(df)

    if ghost is None:
        st.info("Not enough conversation transitions found for ghost analysis.")
        return
    # ── Disclaimer Section ──
    disclaimer_text = (
        "This algorithm is a cold, heartless robot. It measures raw time gaps between different speakers—it "
        "cannot read human context."
        "<ul>"
        "<li><b>The 'False' Ghost:</b> If someone said <i>'See you tomorrow!'</i> and the chat ended, a new message sent "
        "3 days later will register as a 3-day ghosting offense for whoever replied next.</li>"
        "<li><b>The 'Ultra Ghost' & 'Most Ignored' Trap:</b> If you drop a link, a meme, or a closing statement that "
        "requires zero reply, anyone who drops a completely fresh message days later will be blamed as an "
        "<b>Ultra Ghoster</b>, while you get crowned as <b>Most Ignored</b>.</li>"
        "</ul>"
        "Before you end a friendship or block a number over these metrics, verify your case files! "
        "Scroll down to the <b>Worst Ghosting Pairs</b> and use the <b>Complete Ghosting Evidence Log</b> to "
        "see if you were actually left on read or if the conversation had just reached its natural conclusion."
    )
    styles.render_disclaimer(
        title="READ BEFORE ACCUSING ANYONE (The Legal Disclaimer)",
        text_html=disclaimer_text,
        icon="🚨",
        color="#EF4444"
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)


    # ── Row 1: Top 3 Ghost Metrics ──
    col1, col2, col3 = st.columns(3)

    with col1:
        ex = ghost["biggest_example"]
        evidence = [
            "🚨 Wanted for emotional neglect. Basically belongs on a milk carton.",
            f'💬 {ex["prev_sender"]}: "{str(ex["prev_message"])[:35]}..."',
            f'↩️ {ex["reply_sender"]}: "{str(ex["reply_message"])[:35]}..."',
        ]
        styles.render_ghost_card(
            icon="👻",
            title="BIGGEST GHOSTER",
            suspect=ghost["biggest_ghoster"],
            avg_time=f"Avg vanishing: {ghost_mode.format_ghost_time(ghost['biggest_ghoster_time'])}",
            evidence_lines=evidence,
            color="#06B6D4",
        )

    with col2:
        ex = ghost["fastest_example"]
        evidence = [
            "❤️ Down tremendously. Responds before you can even close the app.",
            f'💬 {ex["prev_sender"]}: "{str(ex["prev_message"])[:35]}..."',
            f'↩️ {ex["reply_sender"]}: "{str(ex["reply_message"])[:35]}..."',
        ]
        styles.render_ghost_card(
            icon="⚡",
            title="FASTEST RESPONDER",
            suspect=ghost["fastest"],
            avg_time=f"Panic typing speed: {ghost_mode.format_ghost_time(ghost['fastest_time'])}",
            evidence_lines=evidence,
            color="#10B981",
        )

    with col3:
        if ghost["ultra_example"] is not None:
            ex = ghost["ultra_example"]
            evidence = [
                "⚠️ Legally dead. Vanished into thin air for over a full day.",
                f'💬 {ex["prev_sender"]}: "{str(ex["prev_message"])[:35]}..."',
                f'↩️ {ex["reply_sender"]}: "{str(ex["reply_message"])[:35]}..."',
            ]
        else:
            evidence = ["Absolute miracle. Nobody went radio-silent for over 24 hours."]
            
        styles.render_ghost_card(
            icon="💀",
            title="ULTRA GHOST (24H+)",
            suspect=ghost["ultra_person"],
            avg_time=f"{ghost['ultra_count']} straight desertions",
            evidence_lines=evidence,
            color="#EF4444",
        )

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # ── Row 2: Most Ignored + Longest Ghost ──
    col4, col5 = st.columns(2)

    with col4:
        styles.render_ghost_card(
            icon="🥲",
            title="MOST IGNORED",
            suspect=ghost["ignored_person"],
            avg_time=f"{ghost['ignored_count']} times left on read",
            evidence_lines=[f"💔 Pour one out. Typing sweet entries straight into the void while the chat collective goes blind."],
            color="#EC4899",
        )

    with col5:
        longest = ghost["longest"]
        styles.render_ghost_card(
            icon="🏆",
            title="LONGEST GHOST EVER",
            suspect=f'{longest["prev_sender"]} → {longest["reply_sender"]}',
            avg_time=f"Ice age lasted: {ghost_mode.format_ghost_time(longest['ghost_seconds'])}",
            evidence_lines=[
                "🕰️ Kingdoms fell and seasons changed before this response dropped:",
                f'💬 {longest["prev_time"]}: "{str(longest["prev_message"])[:35]}..."',
                f'↩️ {longest["reply_time"]}: "{str(longest["reply_message"])[:35]}..."',
            ],
            color="#F59E0B",
        )

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # ── Evidence tables ──
    

    styles.render_section_header("🤝", "Worst Ghosting Pairs", "Who ignores whom the most frequently")
    st.dataframe(ghost["pair_stats"], use_container_width=True)

    with st.expander("📋 View Complete Ghosting Evidence", expanded=False):
        st.dataframe(ghost["verification"], use_container_width=True, height=450)