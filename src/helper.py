from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user,df):
    if selected_user != 'All':
        df = df[df['Sender'] == selected_user]
    # Fetch total messages
    num_messages = df.shape[0]

    # Fetch total words
    words = []
    for message in df['Message']:
        words.extend(message.split())
    num_words = len(words)


    #Fetch total media messages
    num_media_messages = df[df['Message'] == '<Media omitted>\n'].shape[0]

    # Fetch total URLs
    extractor = URLExtract()
    urls = []
    for message in df['Message']:
        urls.extend(extractor.find_urls(message))
    num_urls = len(urls)

    return num_messages, num_words, num_urls, num_media_messages

def most_busy_user(df):
    x = df['Sender'].value_counts().head()
    df = round((df['Sender'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'Sender': 'Name', 'count': 'Percentage'})
    return x, df

def remove_stopwords(message):
    with open('src/stopwords_list.txt', 'r') as f:
        stopwords = f.read().splitlines()
    y = []
    for word in message.lower().split():
        if word not in stopwords:
            y.append(word)
    return " ".join(y)

def create_wordcloud(selected_user,df):
    with open('src/stopwords_list.txt', 'r') as f:
        stopwords = f.read().splitlines()
    if selected_user != 'All':
        df = df[df['Sender'] == selected_user]
    temp = df[df['Message'] != '<Media omitted>\n']
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    # 1. Filter out media messages and create a clean copy
    temp = df[df['Message'] != '<Media omitted>\n'].copy()
    
    # 2. Filter by user if a specific user is selected
    if selected_user != 'All':
        temp = temp[temp['Sender'] == selected_user]

    # 3. Remove stopwords
    # Assuming remove_stopwords is defined and returns a string
    temp['Message'] = temp['Message'].apply(remove_stopwords)

    # 4. Tokenize: Convert each message string into a list of words
    temp['Word_List'] = temp['Message'].apply(lambda msg: str(msg).split())

    # 5. Explode: Create a new row for every single word, keeping the Sender attached
    words_df = temp.explode('Word_List')
    
    # Clean up empty rows
    words_df = words_df.dropna(subset=['Word_List'])
    
    if words_df.empty:
         return pd.DataFrame(columns=['Word', 'Count', 'Sender'])

    # 6. Find the top 20 most frequent words overall 
    # (We limit to 20 so the chart doesn't become impossibly tall)
    top_words = words_df['Word_List'].value_counts().head(20).index.tolist()

    # 7. Filter the exploded dataframe to ONLY include those top words
    top_words_df = words_df[words_df['Word_List'].isin(top_words)]

    # 8. Group by both Word and Sender to get the final counts
    most_common_df = top_words_df.groupby(['Word_List', 'Sender']).size().reset_index(name='Count')
    most_common_df = most_common_df.rename(columns={'Word_List': 'Word'})

    return most_common_df

def emoji_helper(selected_user, df):
    # 1. Extract emojis as a list for every single message row
    df['Emoji_List'] = df['Message'].apply(lambda msg: [e['emoji'] for e in emoji.emoji_list(str(msg))])
    
    # 2. Explode the DataFrame so each emoji gets its own row while keeping its Sender
    exploded_df = df.explode('Emoji_List')
    
    # 3. Drop rows where no emojis were found (they will show up as NaN)
    exploded_df = exploded_df.dropna(subset=['Emoji_List'])
    
    # 4. Apply the user filter if a specific user is selected
    if selected_user != 'All':
        exploded_df = exploded_df[exploded_df['Sender'] == selected_user]
        
    # 5. Group by BOTH Sender and Emoji to get individual counts
    emoji_counts = exploded_df.groupby(['Sender', 'Emoji_List']).size().reset_index(name='Count')
    
    # 6. Rename the emoji column for clean display
    emoji_counts = emoji_counts.rename(columns={'Emoji_List': 'Emoji'})
    
    # 7. Sort by Count so the most popular emojis appear first
    emoji_counts = emoji_counts.sort_values(by='Count', ascending=False).reset_index(drop=True)
    
    return emoji_counts

def monthly_timeline(selected_user,df):

    if selected_user != 'All':
        df = df[df['Sender'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'All':
        df = df[df['Sender'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['Message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'All':
        df = df[df['Sender'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'All':
        df = df[df['Sender'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'All':
        df = df[df['Sender'] == selected_user]

    # Ensure seaborn heatmap doesn't crash on empty pivots
    if df.empty:
        days = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday',
        ]
        periods = []
        for h in range(0, 24):
            if h == 23:
                periods.append('23-00')
            elif h == 0:
                periods.append('00-1')
            else:
                periods.append(f'{h}-{h + 1}')


        user_heatmap = pd.DataFrame(0, index=days, columns=periods)
        return user_heatmap

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap






