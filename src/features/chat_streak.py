import pandas as pd


def chat_streak_analysis(df):

    # Get unique chat dates
    dates = (
        pd.to_datetime(df['only_date'])
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )

    if dates.empty:
        return None


    # Longest streak
  
    longest_streak = 1
    current_streak = 1

    streak_start = dates.iloc[0]
    streak_end = dates.iloc[0]

    longest_start = dates.iloc[0]
    longest_end = dates.iloc[0]

    breaks = []

    for i in range(1, len(dates)):

        gap = (
            dates.iloc[i]
            - dates.iloc[i - 1]
        ).days

        if gap == 1:

            current_streak += 1
            streak_end = dates.iloc[i]

        else:

            breaks.append(gap - 1)

            if current_streak > longest_streak:

                longest_streak = current_streak
                longest_start = streak_start
                longest_end = streak_end

            current_streak = 1
            streak_start = dates.iloc[i]
            streak_end = dates.iloc[i]

    # Final check
    if current_streak > longest_streak:

        longest_streak = current_streak
        longest_start = streak_start
        longest_end = streak_end


    # Current streak
  
    current_chat_streak = 1

    for i in range(
        len(dates)-1,
        0,
        -1
    ):

        gap = (
            dates.iloc[i]
            - dates.iloc[i-1]
        ).days

        if gap == 1:
            current_chat_streak += 1
        else:
            break


    # Biggest break
  
    biggest_break = (
        max(breaks)
        if breaks
        else 0
    )


    # Most active day

    activity = (
        df
        .groupby('only_date')
        .size()
        .sort_values(
            ascending=False
        )
    )

    most_active_day = activity.index[0]
    most_active_count = int(
        activity.iloc[0]
    )


    # Streak dataframe

    streak_df = pd.DataFrame({
        'date': dates
    })

    streak_df['streak'] = 1

    running = 1

    for i in range(
        1,
        len(streak_df)
    ):

        gap = (
            streak_df.loc[i, 'date']
            - streak_df.loc[i-1, 'date']
        ).days

        if gap == 1:
            running += 1
        else:
            running = 1

        streak_df.loc[i, 'streak'] = running

    return {

        'longest_streak':
            longest_streak,

        'longest_start':
            longest_start,

        'longest_end':
            longest_end,

        'current_streak':
            current_chat_streak,

        'biggest_break':
            biggest_break,

        'most_active_day':
            most_active_day,

        'most_active_count':
            most_active_count,

        'streak_df':
            streak_df
    }