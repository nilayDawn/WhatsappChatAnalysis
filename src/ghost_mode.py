import pandas as pd


def format_ghost_time(seconds):

    seconds = int(seconds)

    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    if days:
        return f"{days}d {hours}h"

    if hours:
        return f"{hours}h {minutes}m"

    return f"{minutes}m"


def ghosting_analysis(df):

    temp = (
        df
        .sort_values('DateTime')
        .copy()
    )

    # Previous context
    temp['prev_sender'] = temp['Sender'].shift()
    temp['prev_time'] = temp['DateTime'].shift()
    temp['prev_message'] = temp['Message'].shift()

    temp['reply_sender'] = temp['Sender']
    temp['reply_time'] = temp['DateTime']
    temp['reply_message'] = temp['Message']

    temp = temp.dropna(
        subset=[
            'prev_sender',
            'prev_time'
        ]
    )

    # Only real replies
    temp = temp[
        temp['Sender']
        != temp['prev_sender']
    ]

    temp['ghost_seconds'] = (
        temp['reply_time']
        -
        temp['prev_time']
    ).dt.total_seconds()

    if temp.empty:
        return None

    
    # Biggest Ghoster
    

    avg_ghost = (
        temp
        .groupby('reply_sender')
        ['ghost_seconds']
        .mean()
        .sort_values(
            ascending=False
        )
    )

    biggest_ghoster = avg_ghost.index[0]

    biggest_ghoster_time = (
        avg_ghost.iloc[0]
    )

    biggest_example = (
        temp[
            temp['reply_sender']
            ==
            biggest_ghoster
        ]
        .sort_values(
            'ghost_seconds',
            ascending=False
        )
        .iloc[0]
        .to_dict()
    )

    
    # Fastest responder
    

    fastest = (
        temp
        .groupby('reply_sender')
        ['ghost_seconds']
        .mean()
        .sort_values()
    )

    fastest_person = fastest.index[0]

    fastest_time = (
        fastest.iloc[0]
    )

    fastest_example = (
        temp[
            temp['reply_sender']
            ==
            fastest_person
        ]
        .sort_values(
            'ghost_seconds'
        )
        .iloc[0]
        .to_dict()
    )

    
    # Longest ghost
    

    longest = temp.loc[
        temp['ghost_seconds']
        .idxmax()
    ].to_dict()

    
    # Most ignored
   

    ignored = (
        temp
        .groupby('prev_sender')
        .size()
        .sort_values(
            ascending=False
        )
    )

    ignored_person = (
        ignored.index[0]
    )

    ignored_count = int(
        ignored.iloc[0]
    )

   
    # Ultra ghost
   

    ultra = temp[
        temp['ghost_seconds']
        > 86400
    ]

    if not ultra.empty:

        ultra_counts = (
            ultra
            .groupby(
                'reply_sender'
            )
            .size()
            .sort_values(
                ascending=False
            )
        )

        ultra_person = (
            ultra_counts.index[0]
        )

        ultra_count = int(
            ultra_counts.iloc[0]
        )

        ultra_example = (
            ultra[
                ultra['reply_sender']
                ==
                ultra_person
            ]
            .sort_values(
                'ghost_seconds',
                ascending=False
            )
            .iloc[0]
            .to_dict()
        )

    else:

        ultra_person = "Nobody"
        ultra_count = 0
        ultra_example = None

  
    # Ghost pair stats
    

    pair_stats = (
        temp
        .groupby(
            [
                'prev_sender',
                'reply_sender'
            ]
        )['ghost_seconds']
        .agg(
            ['mean',
             'max',
             'count']
        )
        .reset_index()
    )

    pair_stats.columns = [
        'Ghosted_By',
        'Replied_By',
        'Average_Ghost',
        'Longest_Ghost',
        'Interactions'
    ]

    pair_stats[
        'Average_Ghost'
    ] = pair_stats[
        'Average_Ghost'
    ].apply(
        format_ghost_time
    )

    pair_stats[
        'Longest_Ghost'
    ] = pair_stats[
        'Longest_Ghost'
    ].apply(
        format_ghost_time
    )

  
    # Verification table
    

    verification = temp[
        [
            'prev_sender',
            'reply_sender',
            'prev_time',
            'reply_time',
            'ghost_seconds',
            'prev_message',
            'reply_message'
        ]
    ].copy()

    verification.columns = [
        'Ghosted_By',
        'Replied_By',
        'Previous_Time',
        'Reply_Time',
        'Ghost_Duration',
        'Previous_Message',
        'Reply_Message'
    ]

    verification[
        'Ghost_Duration'
    ] = verification[
        'Ghost_Duration'
    ].apply(
        format_ghost_time
    )

    verification = (
        verification
        .sort_values(
            'Previous_Time',
            ascending=False
        )
    )

    return {

       
        # Biggest Ghoster
      
        'biggest_ghoster':
            biggest_ghoster,

        'biggest_ghoster_time':
            biggest_ghoster_time,

        'biggest_example':
            biggest_example,

       
        # Fastest
      
        'fastest':
            fastest_person,

        'fastest_time':
            fastest_time,

        'fastest_example':
            fastest_example,

    
        # Longest ghost
     
        'longest':
            longest,

   
        # Most ignored
      
        'ignored_person':
            ignored_person,

        'ignored_count':
            ignored_count,

   
        # Ultra ghost
       
        'ultra_person':
            ultra_person,

        'ultra_count':
            ultra_count,

        'ultra_example':
            ultra_example,

    
        # Tables
      
        'pair_stats':
            pair_stats,

        'verification':
            verification
    }