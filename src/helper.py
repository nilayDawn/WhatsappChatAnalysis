from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji

MEDIA_TEXT = '<Media omitted>' 

# Load stopwords 
with open('src/full_stopword.txt', 'r', encoding='utf-8') as f:
    STOPWORDS = set(f.read().splitlines())


def filter_user(df, selected_user):
    if selected_user != 'All':
        return df[df['Sender'] == selected_user]
    return df


def create_ngrams(text, n):
    words = str(text).split()
    # Grab chunks of size 'n' and join them with a space
    return [" ".join(words[i:i+n]) for i in range(len(words) - n + 1)]


def fetch_stats(selected_user, df):
    df = filter_user(df, selected_user)

    # total messages
    num_messages = df.shape[0]

    # total words
    num_words = sum(len(str(message).split()) for message in df['Message'])

    # media messages
    num_media_messages = (df['is_media'] == True).sum()

    # urls
    extractor = URLExtract()
    num_urls = sum(len(extractor.find_urls(str(message)))for message in df['Message'])

    return num_messages, num_words, num_urls, num_media_messages


def most_busy_user(df):
    x = df['Sender'].value_counts().head()

    percent_df = (
        round((df['Sender'].value_counts() / df.shape[0]) * 100, 2)
        .reset_index()
        .rename(columns={
            'Sender': 'Name',
            'count': 'Percentage'
        })
    )

    return x, percent_df


def remove_stopwords(message):
    return " ".join(
        word
        for word in str(message).lower().split()
        if word not in STOPWORDS
    )


def create_wordcloud(selected_user, df):
    df = filter_user(df, selected_user)

    temp = df[df['Message'] != MEDIA_TEXT].copy()

    wc = WordCloud(
        width=800,
        height=450,
        min_font_size=10,
        background_color="#ffffff",
        colormap='plasma'
    )

    temp['Message'] = temp['Message'].apply(remove_stopwords)

    df_wc = wc.generate(
        temp['Message'].str.cat(sep=" ")
    )

    return df_wc


def create_wordcloud_bigrams(selected_user, df):

    temp = df[df['Message'] != MEDIA_TEXT].copy()
    temp = filter_user(temp, selected_user)

    temp['Message'] = temp['Message'].apply(remove_stopwords)

    temp['Bigram_List'] = temp['Message'].apply(create_ngrams, n=2)

    exploded_bigrams = (
        temp
        .explode('Bigram_List')['Bigram_List']
        .dropna()
    )

    bigram_frequencies = (
        exploded_bigrams
        .value_counts()
        .to_dict()
    )

    if not bigram_frequencies:
        return None

    wc = WordCloud(
        width=800,
        height=450,
        min_font_size=10,
        background_color="#ffffff",
        colormap='plasma'
    )

    df_wc = wc.generate_from_frequencies(
        bigram_frequencies
    )

    return df_wc


def most_common_words(selected_user, df):

    temp = df[df['Message'] != MEDIA_TEXT].copy()
    temp = filter_user(temp, selected_user)

    temp['Message'] = temp['Message'].apply(
        remove_stopwords
    )

    temp['Word_List'] = temp['Message'].apply(create_ngrams, n=2)

    words_df = temp.explode('Word_List')

    words_df = words_df.dropna(
        subset=['Word_List']
    )

    if words_df.empty:
        empty_top20 = pd.DataFrame(
            columns=['Word', 'Count', 'Sender']
        )

        empty_all = pd.DataFrame(
            columns=['TopWords', 'Count', 'Sender']
        )

        return empty_top20, empty_all

    all_words_df = (
        words_df
        .groupby(['Word_List', 'Sender'])
        .size()
        .reset_index(name='Count')
    )

    all_words_df = all_words_df.rename(
        columns={'Word_List': 'TopWords'}
    )

    all_words_df = (
        all_words_df
        .sort_values(
            by='Count',
            ascending=False
        )
        .reset_index(drop=True)
    )

    all_words_df = all_words_df.head(50)

    top_words = (
        words_df['Word_List']
        .value_counts()
        .head(20)
        .index
        .tolist()
    )

    top_words_df = words_df[
        words_df['Word_List'].isin(top_words)
    ]

    most_common_df = (
        top_words_df
        .groupby(['Word_List', 'Sender'])
        .size()
        .reset_index(name='Count')
    )

    most_common_df = most_common_df.rename(
        columns={'Word_List': 'Word'}
    )

    return most_common_df, all_words_df


def emoji_helper(selected_user, df):

    temp = df.copy()

    temp['Emoji_List'] = temp['Message'].apply(
        lambda msg: [ e['emoji'] for e in emoji.emoji_list(str(msg))])

    exploded_df = temp.explode('Emoji_List')

    exploded_df = exploded_df.dropna(
        subset=['Emoji_List']
    )

    exploded_df = filter_user(
        exploded_df,
        selected_user
    )

    emoji_counts = (
        exploded_df
        .groupby(['Sender', 'Emoji_List'])
        .size()
        .reset_index(name='Count')
    )

    emoji_counts = emoji_counts.rename(
        columns={'Emoji_List': 'Emoji'}
    )

    emoji_counts = (
        emoji_counts
        .sort_values(
            by='Count',
            ascending=False
        )
        .reset_index(drop=True)
    )

    return emoji_counts


def monthly_timeline(selected_user, df):

    df = filter_user(df, selected_user)

    timeline = (
        df.groupby(
            ['year', 'month_num', 'month']
        )
        .count()['Message']
        .reset_index()
    )

    timeline['time'] = (
        timeline['month']
        + "-"
        + timeline['year'].astype(str)
    )

    return timeline


def daily_timeline(selected_user, df):

    df = filter_user(df, selected_user)

    daily_timeline = (
        df.groupby('only_date')
        .count()['Message']
        .reset_index()
    )

    return daily_timeline


def week_activity_map(selected_user, df):

    df = filter_user(df, selected_user)

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):

    df = filter_user(df, selected_user)

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):

    df = filter_user(df, selected_user)

    if df.empty:
        days = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ]

        periods = []

        for h in range(24):
            if h == 23:
                periods.append('23-00')
            elif h == 0:
                periods.append('00-1')
            else:
                periods.append(f'{h}-{h+1}')

        return pd.DataFrame(
            0,
            index=days,
            columns=periods
        )

    user_heatmap = (
        df.pivot_table(
            index='day_name',
            columns='period',
            values='Message',
            aggfunc='count'
        )
        .fillna(0)
    )

    return user_heatmap