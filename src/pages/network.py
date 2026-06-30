import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import features.reply_network as reply_network
import styles


def render(df):
    """Chapter 4: Reply Network — Social network graph with glowing nodes."""

    styles.render_chapter_divider("04", "Reply Network")

    styles.render_section_header("🕸️", "The Social Web",
                                 "Who's really talking to whom? A friendship graph.")

    reply_data = reply_network.reply_network_analysis(df)
    edges = reply_data["edges"]

    if edges.empty:
        st.info("Not enough replies found to build a network.")
        return

    # ── Award cards ──
    col1, col2, col3 = st.columns(3)
    with col1:
        styles.render_metric_card(
            "Most Popular", reply_data["most_popular"],
            "Most replied to", "🏆", "#F59E0B",
        )
    with col2:
        styles.render_metric_card(
            "Most Responsive", reply_data["most_responsive"],
            "Most replies sent", "⚡", "#8B5CF6",
        )
    with col3:
        styles.render_metric_card(
            "Social Butterfly", reply_data["social_butterfly"],
            "Most connections", "🦋", "#EC4899",
        )

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # ── Network graph — dark background with glowing nodes ──
    G = nx.DiGraph()
    for _, row in edges.iterrows():
        G.add_edge(row["From"], row["To"], weight=row["Replies"])

    fig, ax = plt.subplots(figsize=(10, 7.5))
    fig.patch.set_facecolor("#070B14")
    ax.set_facecolor("#070B14")

    pos = nx.circular_layout(G)
    weights = [G[u][v]["weight"] for u, v in G.edges()]
    widths = [max(1.5, min(8.0, w / 3)) for w in weights]

    # Glowing nodes
    nx.draw_networkx_nodes(
        G, pos, node_size=3200,
        node_color="#8B5CF6", alpha=0.3, ax=ax,
    )
    nx.draw_networkx_nodes(
        G, pos, node_size=2400,
        node_color="#8B5CF6", edgecolors="#c4b5fd",
        linewidths=2, ax=ax,
    )

    # Glowing edges
    nx.draw_networkx_edges(
        G, pos, width=[w * 1.5 for w in widths], arrows=False,
        edge_color="#8B5CF6", alpha=0.15, connectionstyle="arc3,rad=0.15", ax=ax,
    )
    nx.draw_networkx_edges(
        G, pos, width=widths, arrows=True, arrowsize=18,
        edge_color="#c4b5fd", alpha=0.7, connectionstyle="arc3,rad=0.15", ax=ax,
    )

    # Labels
    nx.draw_networkx_labels(
        G, pos, font_size=10, font_weight="bold", font_color="#f1f5f9", ax=ax,
    )
    edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_size=9, font_color="#c4b5fd",
        bbox=dict(facecolor="#0F172A", edgecolor="#8B5CF6", alpha=0.8,
                  boxstyle="round,pad=0.3"),
        ax=ax,
    )
    ax.axis("off")

    col_graph, col_table = st.columns([3, 2])
    with col_graph:
        st.pyplot(fig)
        plt.close(fig)
    with col_table:
        st.markdown(
            "<div style='font-weight:700;color:#8B5CF6;font-size:1.05rem;margin-bottom:10px;'>"
            "📋 Reply Matrix</div>",
            unsafe_allow_html=True,
        )
        st.dataframe(
            edges.sort_values("Replies", ascending=False),
            use_container_width=True,
        )
