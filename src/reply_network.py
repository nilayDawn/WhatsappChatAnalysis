def reply_network_analysis(df):

    # Sort chronologically
    temp = df.sort_values('DateTime').copy()

    # Previous sender and time
    temp['prev_sender'] = temp['Sender'].shift()
    temp['prev_time'] = temp['DateTime'].shift()

    # Time gap
    temp['reply_gap'] = (
        temp['DateTime']
        - temp['prev_time']
    ).dt.total_seconds()

    # Remove first row
    temp = temp.dropna(subset=['prev_sender'])

    # Remove self replies
    temp = temp[
        temp['Sender']
        != temp['prev_sender']
    ]

    # Remove unrealistic reply gaps
    temp = temp[
        temp['reply_gap']
        <= 3600          # 1 hour
    ]

    # Build reply edges
    edges = (
        temp
        .groupby(
            ['prev_sender', 'Sender']
        )
        .size()
        .reset_index(name='Replies')
    )

    edges.columns = [
        'From',
        'To',
        'Replies'
    ]

    # Most popular
    incoming = (
        edges
        .groupby('To')['Replies']
        .sum()
        .sort_values(ascending=False)
    )

    # Most responsive
    outgoing = (
        edges
        .groupby('From')['Replies']
        .sum()
        .sort_values(ascending=False)
    )

    # Social butterfly
    connections = {}

    users = df['Sender'].unique()

    for user in users:

        outgoing_users = set(
            edges[
                edges['From'] == user
            ]['To']
        )

        incoming_users = set(
            edges[
                edges['To'] == user
            ]['From']
        )

        connections[user] = len(
            outgoing_users |
            incoming_users
        )

    return {
        "edges": edges,
        "most_popular": (
            incoming.index[0]
            if not incoming.empty else None
        ),
        "most_responsive": (
            outgoing.index[0]
            if not outgoing.empty else None
        ),
        "social_butterfly": (
            max(connections,
                key=connections.get)
            if connections else None
        ),
        "incoming": incoming,
        "outgoing": outgoing,
        "connections": connections
    }