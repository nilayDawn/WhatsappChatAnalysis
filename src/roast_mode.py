import pandas as pd
import emoji


def roast_mode(df):

    if df.empty:
        return None

    temp = df.copy()
    total_messages = len(temp)

    # Message Spammer
  
    msg_counts = temp['Sender'].value_counts()

    spammer = msg_counts.index[0]
    spammer_percent = round(
        msg_counts.iloc[0] / total_messages * 100,
        1
    )

   
    # Silent Observer
  
    silent = msg_counts.index[-1]
    silent_percent = round(
        msg_counts.iloc[-1] / total_messages * 100,
        1
    )

    # Essay Writer
  
    temp['word_count'] = (
        temp['Message']
        .astype(str)
        .str.split()
        .str.len()
    )

    essay_stats = (
        temp
        .groupby('Sender')['word_count']
        .mean()
        .sort_values(ascending=False)
    )

    essay_writer = essay_stats.index[0]
    essay_score = round(
        essay_stats.iloc[0],
        1
    )

    # Speed Demon
  
    reply = temp.copy()

    reply['prev_sender'] = reply['Sender'].shift()
    reply['prev_time'] = reply['DateTime'].shift()

    reply['reply_seconds'] = (
        reply['DateTime']
        - reply['prev_time']
    ).dt.total_seconds()

    reply = reply[
        (reply['Sender'] != reply['prev_sender'])
        &
        (reply['reply_seconds'] > 0)
        &
        (reply['reply_seconds'] <= 3600)
    ]

    if not reply.empty:

        speed = (
            reply
            .groupby('Sender')
            ['reply_seconds']
            .mean()
            .sort_values()
        )

        speed_demon = speed.index[0]

        speed_value = (
            f"{int(speed.iloc[0])} sec"
        )

    else:

        speed_demon = "Nobody"
        speed_value = "-"

   
    # Double Texter
  
    temp['prev_sender'] = (
        temp['Sender']
        .shift()
    )

    temp['double'] = (
        temp['Sender']
        ==
        temp['prev_sender']
    )

    doubles = (
        temp
        .groupby('Sender')
        ['double']
        .sum()
        .sort_values(
            ascending=False
        )
    )

    double_texter = doubles.index[0]
    double_count = int(
        doubles.iloc[0]
    )

    
    # Emoji Addict
    
    temp['emoji_count'] = (
        temp['Message']
        .apply(
            lambda x:
            len(
                emoji.emoji_list(
                    str(x)
                )
            )
        )
    )

    emoji_stats = (
        temp
        .groupby('Sender')
        ['emoji_count']
        .sum()
        .sort_values(
            ascending=False
        )
    )

    emoji_addict = emoji_stats.index[0]
    emoji_total = int(
        emoji_stats.iloc[0]
    )

   
    # Night Owl
   
    night = temp[
        (temp['hour'] >= 0)
        &
        (temp['hour'] <= 4)
    ]

    if not night.empty:

        night_counts = (
            night['Sender']
            .value_counts()
        )

        night_owl = night_counts.index[0]

        night_percent = round(
            night_counts.iloc[0]
            /
            len(night)
            * 100,
            1
        )

    else:

        night_owl = "Nobody"
        night_percent = 0

    
    # NPC Speaker
  
    npc = (
        temp
        .groupby('Sender')
        ['word_count']
        .mean()
        .sort_values()
    )

    npc_person = npc.index[0]
    npc_words = round(
        npc.iloc[0],
        1
    )

  
# Final Roast Dictionary
    roasts = {
        "📢 The Spammer": {
            "winner": spammer,
            "value": f"{spammer_percent}% of chat",
            "roast": f"Responsible for {spammer_percent}% of the total volume. Treat this chat like your personal diary much, {spammer}? The rest of us are just background extras in your story."
        },

        "👻 Silent Observer": {
            "winner": silent,
            "value": f"{silent_percent}% of chat",
            "roast": f"Contributing a whopping {silent_percent}%. {silent} is definitely in a witness protection program, or just lurking in the shadows collecting modern art screenshots to blackmail us later."
        },

        "📝 Essay Writer": {
            "winner": essay_writer,
            "value": f"{essay_score} words/msg",
            "roast": f"Averages {essay_score} words per message. {essay_writer} doesn't send texts; they publish unedited memoirs. We need a cup of coffee and a quiet room just to open your notifications."
        },

        "⚡ Speed Demon": {
            "winner": speed_demon,
            "value": speed_value,
            "roast": f"Average response time: {speed_value}. {speed_demon} is hovering over the screen 24/7 like an absolute psycho. Please put the phone down, the world outside is beautiful."
        },

        "💀 Double Texter": {
            "winner": double_texter,
            "value": f"{double_count} times",
            "roast": f"Sent a secondary message {double_count} times because waiting for a reply is physically painful. The desperate 'hello?' energy is radiant, {double_texter}."
        },

        "🤡 Emoji King": {
            "winner": emoji_addict,
            "value": f"{emoji_total} emojis",
            "roast": f"Dropped {emoji_total} emojis because raw language is too hard. {emoji_addict}'s keyboard is 90% hieroglyphics. Go back to kindergarten and learn human vocabulary."
        },

        "🌙 Night Owl": {
            "winner": night_owl,
            "value": f"{night_percent}% of late nights",
            "roast": f"Owns {night_percent}% of the unhinged 2:00 AM bandwidth. {night_owl}'s circadian rhythm is completely fictional. Sleep is optional, sleep-deprived thoughts are mandatory."
        },

        "🤖 NPC Speaker": {
            "winner": npc_person,
            "value": f"{npc_words} words/msg",
            "roast": f"Averages {npc_words} words. {npc_person} uses fewer bytes than a floppy disk. 'K', 'ok', 'nice'. Truly the background NPC of this entire conversation."
        }
    }

    return roasts