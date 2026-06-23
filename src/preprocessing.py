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

    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='mixed', dayfirst=True)

    df["Year"] = df["DateTime"].dt.year
    df["Month"] = df["DateTime"].dt.month_name()
    df["Day"] = df["DateTime"].dt.day
    df["Hour"] = df["DateTime"].dt.hour
    df["Minute"] = df["DateTime"].dt.minute    

    return df

if __name__ == "__main__":
    with open("Chats/WhatsApp Chat with ML project.txt", "r", encoding="utf-8") as f:
        text = f.read()
    df = preprocess(text)
    print(df.head())