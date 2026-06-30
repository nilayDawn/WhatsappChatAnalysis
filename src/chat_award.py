import emoji
from urlextract import URLExtract


def chat_awards(df):

    awards = {}


    # Chatterbox

    chatterbox = df['Sender'].value_counts()

    if not chatterbox.empty:
        awards['chatterbox'] = {
            'title': '👑 Chatterbox',
            'winner': chatterbox.index[0],
            'value': int(chatterbox.iloc[0]),
            'suffix': 'messages',
            'description': 'The most prolific chatter in the group. Your notifications are constantly buzzing because of this person.'
        }


    # Paparazzi

    media = (
        df[df['is_media']]
        ['Sender']
        .value_counts()
    )

    if not media.empty:
        awards['paparazzi'] = {
            'title': '📸 Paparazzi',
            'winner': media.index[0],
            'value': int(media.iloc[0]),
            'suffix': 'media files',
            'description': 'Most media files shared in the chat.The sole reason your phone is always out of storage.'
        }

    # Night owl

    night = df[
        (df['hour'] >= 23) |
        (df['hour'] <= 4)
    ]

    night_count = night['Sender'].value_counts()

    if not night_count.empty:
        awards['nightowl'] = {
            'title': '🌙 Night Owl',
            'winner': night_count.index[0],
            'value': int(night_count.iloc[0]),
            'suffix': 'late-night messages',
            'description': 'Only wakes up when the rest of the group is asleep. Lives to drop unhinged, 3:00 AM thoughts that ruin your morning notifications.'
        }


    # Essay writer

    avg_words = (
        df.groupby('Sender')['word_count']
        .mean()
        .sort_values(ascending=False)
    )

    if not avg_words.empty:
        awards['essay'] = {
            'title': '📝 Essay Writer',
            'winner': avg_words.index[0],
            'value': round(avg_words.iloc[0],1),
            'suffix': 'words/msg',
            'description': 'The group\'s most verbose member. Writes long, detailed messages that are often ignored.'
        }
    emoji_count = {}

    for _, row in df.iterrows():

        sender = row['Sender']

        count = len(
            emoji.emoji_list(
                str(row['Message'])
            )
        )

        emoji_count[sender] = (
            emoji_count.get(sender,0)
            + count
        )

    if emoji_count:

        winner = max(
            emoji_count,
            key=emoji_count.get
        )

        awards['emoji'] = {
            'title': '😂 Emoji King',
            'winner': winner,
            'value': emoji_count[winner],
            'suffix': 'emojis',
            'description':'The group\'s most expressive member. Uses emojis to convey emotions, reactions, and sometimes entire messages.'
        }


    # Link addict
  
    extractor = URLExtract()

    url_count = {}

    for _, row in df.iterrows():

        sender = row['Sender']

        urls = extractor.find_urls(
            str(row['Message'])
        )

        url_count[sender] = (
            url_count.get(sender,0)
            + len(urls)
        )

    if url_count:

        winner = max(
            url_count,
            key=url_count.get
        )

        awards['link'] = {
            'title': '🔗 Link Addict',
            'winner': winner,
            'value': url_count[winner],
            'suffix': 'links',
            'description': 'The group\'s most connected member. Shares links to articles, videos, and other content, keeping the group informed and entertained.'
        }

    return awards