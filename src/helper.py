from urlextract import URLExtract
from wordcloud import WordCloud

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

def create_wordcloud(selected_user,df):
    with open('src/stopwords_list.txt', 'r') as f:
        stopwords = f.read().splitlines()
    if selected_user != 'All':
        df = df[df['Sender'] == selected_user]
    temp = df[df['Message'] != '<Media omitted>\n']

    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
    return df_wc