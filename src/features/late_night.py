import pandas as pd


def late_night_analysis(df):

    temp = df.copy()

    # Define night hours
    night = temp[
        (temp['hour'] >= 0)
        &
        (temp['hour'] <= 5)
    ].copy()

    if night.empty:
        return None

    
    # Night owl
    

    night_counts = (
        night['Sender']
        .value_counts()
    )

    night_owl = night_counts.index[0]
    night_owl_count = int(
        night_counts.iloc[0]
    )

    
    # Best sleeper
    

    total = (
        temp
        .groupby('Sender')
        .size()
    )

    night_total = (
        night
        .groupby('Sender')
        .size()
    )

    sleep_ratio = (
        night_total
        / total
        * 100
    ).fillna(0)

    sleep_ratio = (
        sleep_ratio
        .sort_values()
    )

    best_sleeper = sleep_ratio.index[0]
    best_score = round(
        sleep_ratio.iloc[0],
        1
    )

    worst_sleeper = sleep_ratio.index[-1]
    worst_score = round(
        sleep_ratio.iloc[-1],
        1
    )

    
    # Demon hour
    

    hour_stats = (
        night['hour']
        .value_counts()
        .sort_values(
            ascending=False
        )
    )

    demon_hour = int(
        hour_stats.index[0]
    )

    demon_count = int(
        hour_stats.iloc[0]
    )

    
    # Longest night session
    

    night = (
        night
        .sort_values(
            'DateTime'
        )
        .copy()
    )

    night['gap'] = (
        night['DateTime']
        .diff()
        .dt.total_seconds()
        .fillna(0)
    )

    night['session'] = (
        night['gap']
        > 3600
    ).cumsum()

    sessions = []

    for _, group in night.groupby('session'):

        if len(group) < 2:
            continue

        duration = (
            group['DateTime'].max()
            -
            group['DateTime'].min()
        )

        sessions.append({

            'start':
                group['DateTime'].min(),

            'end':
                group['DateTime'].max(),

            'messages':
                len(group),

            'duration':
                duration
        })

    if sessions:

        longest_session = max(
            sessions,
            key=lambda x:
            x['duration']
        )

    else:

        longest_session = None

    
    # Sleep debt
    

    total_night = len(night)

    sleep_hours = round(
        total_night / 30,
        1
    )

    sleep_days = round(
        sleep_hours / 24,
        1
    )

    
    # Personality type (Fixed Logic)
    
    personalities = {}
    total_night_messages = len(night)

    # Iterate through all users in the chat
    for user in total.index:
        
        # Get their raw count of night messages (default to 0 if none)
        night_msgs = night_total.get(user, 0)
        
        # Calculate their percentage of the GROUP'S total night messages
        if total_night_messages > 0:
            night_share = (night_msgs / total_night_messages) * 100
        else:
            night_share = 0

        # Assign diagnoses based on how much of the night chat they dominate
        if night_msgs == 0:
            personalities[user] = "😇 Literal Angel (Sleeps at night)"
        elif night_share < 10:
            personalities[user] = "☀️ Functioning Adult (Boring)"
        elif night_share < 25:
            personalities[user] = "🦉 Standard Night Owl"
        elif night_share < 50:
            personalities[user] = "🧟 Caffeine-Powered Zombie"
        else:
            personalities[user] = "👹 Nocturnal Chaos Goblin"

    
    # Heatmap
    

    heatmap = (
        night
        .pivot_table(
            index='Sender',
            columns='hour',
            values='Message',
            aggfunc='count'
        )
        .fillna(0)
    )

    
    # Leaderboard
    

    leaderboard = (
        night_counts
        .reset_index()
    )

    leaderboard.columns = [
        'User',
        'Night_Messages'
    ]

    
    return {

        'night_owl':
            night_owl,

        'night_owl_count':
            night_owl_count,

        'best_sleeper':
            best_sleeper,

        'best_score':
            best_score,

        'worst_sleeper':
            worst_sleeper,

        'worst_score':
            worst_score,

        'demon_hour':
            demon_hour,

        'demon_count':
            demon_count,

        'longest_session':
            longest_session,

        'sleep_hours':
            sleep_hours,

        'sleep_days':
            sleep_days,

        'personalities':
            personalities,

        'leaderboard':
            leaderboard,

        'heatmap':
            heatmap
    }