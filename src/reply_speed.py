def response_time_analysis(df):

    # sort chronologically
    temp = df.sort_values('DateTime').copy()

    # previous sender
    temp['prev_sender'] = temp['Sender'].shift()

    # previous message time
    temp['prev_time'] = temp['DateTime'].shift()

    # calculate difference
    temp['response_seconds'] = (
        temp['DateTime'] - temp['prev_time']
    ).dt.total_seconds()

    # keep only actual replies
    temp = temp[
        temp['Sender'] != temp['prev_sender']
    ]

    # remove unrealistic gaps
    temp = temp[
        (temp['response_seconds'] > 0)
        &
        (temp['response_seconds'] < 86400)
    ]

    if temp.empty:
        return None

    avg_reply = (
        temp.groupby('Sender')
        ['response_seconds']
        .mean()
        .sort_values()
    )

    fastest = avg_reply.index[0]

    longest = (
        temp.loc[
            temp['response_seconds'].idxmax()
        ]
    )

    return {
        'avg_reply': avg_reply,
        'fastest': fastest,
        'longest_ignore_sender':
            longest['Sender'],
        'longest_ignore':
            longest['response_seconds'],
        'longest_ignore_to': longest['prev_sender'],
        'longest_ignore_time': longest['DateTime'],
    }

#SECOND TIME FORMATTER
def format_seconds(seconds):

    seconds = int(seconds)

    days = seconds // 86400
    seconds %= 86400

    hours = seconds // 3600
    seconds %= 3600

    minutes = seconds // 60
    seconds %= 60

    if days:
        return f"{days}d {hours}h"

    if hours:
        return f"{hours}h {minutes}m"

    if minutes:
        return f"{minutes}m {seconds}s"

    return f"{seconds}s"