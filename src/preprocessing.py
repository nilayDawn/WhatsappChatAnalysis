import re
import pandas as pd


def preprocess(text:str) -> pd.DataFrame:

    # with open(file_object , 'r', encoding='utf-8-sig') as f:
    #     text = f.read()

    #text = file_object.read().decode('utf-8-sig')

    noise_charracters = ['\u202f', '\u2068', '\u2069']
    for char in noise_charracters:
        text = text.replace(char, " ")
    
    # Group 1: Date, Group 2: Time, Group 3: Sender, Group 4: Message
    pattern = r"(\d{2}/\d{2}/\d{2}),\s+(\d{1,2}:\d{2}\s?[ap]m)\s+-\s+(.*?):\s+(.*?)(?=\d{2}/\d{2}/\d{2},|$)"

    # re.DOTALL is important if your messages span multiple lines
    matches = re.findall(pattern, text, re.DOTALL)

    df = pd.DataFrame(matches, columns=['Date', 'Time', 'Sender', 'Message'])   

    # Drops any row containing these phrases, ignoring uppercase/lowercase
    df = df[~df['Message'].str.contains('This message was deleted|You deleted this message', case=False, na=False)]

    # Strip hidden spaces/newlines, then remove rows that start with '<' AND end with '>'
    # Drops any row where a message contains a '<' followed by ANY text, and then a '>'
    df['Message'] = df['Message'].str.replace(r'<.*?>', '', regex=True)

    # Keep only messages that have 30 words or fewer
    df = df[df['Message'].astype(str).str.split().str.len() <= 30]

    # Keep only rows where the message is NOT an empty string
    df = df[df['Message'].str.strip() != ""]

    #keep only the rows where 'Sender' name is <= 5 words
    df = df[df['Sender'].str.split().str.len() <= 5]

    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='mixed', dayfirst=True)

    df['only_date'] = df['DateTime'].dt.date
    df['year'] = df['DateTime'].dt.year
    df['month_num'] = df['DateTime'].dt.month
    df['month'] = df['DateTime'].dt.month_name()
    df['day'] = df['DateTime'].dt.day
    df['day_name'] = df['DateTime'].dt.day_name()
    df['hour'] = df['DateTime'].dt.hour
    df['minute'] = df['DateTime'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

if __name__ == "__main__":
    with open("Chats/WhatsApp Chat with ML project.txt", "r", encoding="utf-8") as f:
        text = f.read()
    df = preprocess(text)
    print(df.head())