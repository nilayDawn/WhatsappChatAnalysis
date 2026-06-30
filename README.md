# 💬 Chat Rewind — Your WhatsApp Story

Discover the hidden story inside your WhatsApp chats. **Chat Rewind** transforms raw chat logs into a cinematic, Spotify Wrapped-style storytelling experience. Uncover friendships, analyze emojis, expose ghosters, track daily streaks, and unlock funny achievements.

🔗 **Live App Link:** [https://whatsapp-chat-analyzer-by-nilaydawn.onrender.com](https://whatsapp-chat-analyzer-by-nilaydawn.onrender.com)

🔗 **Streamlit App Link:** [https://whatsappchatanalysis-by-nilay-dawn.streamlit.app/](https://whatsappchatanalysis-by-nilay-dawn.streamlit.app/)

---

## ✨ Features & Functionality

Chat Rewind analyzes your uploaded `.txt` chat logs and breaks down the data into two main chapters:

### 📖 Your Story (Individual & Global Metrics)
*   **📊 The Overview**: Key statistics including total messages, words, links, active days, and participants, along with a contribution breakdown of who dominates the chat.
*   **🔤 Slang & Catchphrases**: Deep dive into vocabulary size, total unique words, and custom word clouds of the most frequently used terms.
*   **🎭 Emoji & Vibe Check**: Detailed analysis of favorite emojis and a sentiment-based "vibe check" for each user.
*   **📈 When Are We Active?**: Hourly and weekly timeline visualizations to map out your communication schedules and peaks.

### 👥 Group Chapters (All-User Analysis)
*   **🏆 Chat Awards**: Steam-style achievements unlocking badges like *The Novelist* (sends long texts), *Media Spammer* (sends lots of media), *Early Bird*, and *Night Owl*.
*   **⚡ Response Time**: Fast-paced metrics ranking who replies the quickest, average reply latency, and a global response leaderboard.
*   **🕸️ Reply Network**: An interactive social graph detailing exactly who responds to whom most frequently.
*   **🔥 Chat Streaks**: Duolingo-style streak tracking showing your longest/current consecutive messaging streaks alongside humorous relationship statuses (e.g. *💍 Basically Married*, *❤️ Mutual Obsession*, *🪦 Ghosted?*).
*   **😂 Roast Report**: Playful, AI-styled comedic roasts of different participants' texting styles and traits.
*   **👻 Ghosting Analysis**: Detailed detective-grade files revealing your group's biggest vanishing acts, average ignore durations, and "Most Ignored" list, complete with a verified raw evidence table.
*   **🌙 Sleep Deprivation**: An analysis highlighting who's texting at 3 AM and who needs to fix their sleep schedule.

---

## 📖 How to Export Your WhatsApp Chat

1.  Open the desired chat on **WhatsApp** (Mobile or Web).
2.  Tap the options menu (`⋮` or group info) and select **More** → **Export Chat**.
3.  Choose **Without Media** (this will generate a `.txt` file).
4.  If the export is in a `.zip` file, extract it to get the raw `.txt` file.
5.  Upload the `.txt` file directly into **Chat Rewind**!

---

## 🛠️ Local Development & Setup

This project requires **Python 3.12+**. You can set it up locally using standard Python tools or using the ultra-fast Python package installer `uv`.

### Option A: Using `uv` (Recommended)

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/nilayDawn/WhatsappChatAnalysis.git
    cd WhatsappChatAnalysis
    ```

2.  **Install Dependencies and Run:**
    `uv` will automatically create a virtual environment and run the application.
    ```bash
    uv run streamlit run src/app.py
    ```

---

### Option B: Using standard Python `venv` & `pip`

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/nilayDawn/WhatsappChatAnalysis.git
    cd WhatsappChatAnalysis
    ```

2.  **Create and Activate a Virtual Environment:**
    *   **macOS / Linux:**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    *   **Windows:**
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```

    *(Note: The virtual environment can also be configured with `.venv/bin/pip` or `.venv/bin/streamlit` directly.)*

3.  **Install Required Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application:**
    ```bash
    streamlit run src/app.py
    ```

The application will launch in your default web browser at `http://localhost:8501`.

---

## 📦 Core Technology Stack

*   **Frontend / Dashboard UI:** [Streamlit](https://streamlit.io/) with customized glassmorphic styling (`src/css/base.css`).
*   **Data Processing:** [Pandas](https://pandas.pydata.org/) for chat ingestion, regex parsing, and analytics computations.
*   **Data Visualizations:** [Plotly Express](https://plotly.com/python/) and [Wordcloud](https://github.com/amueller/word_cloud).
*   **Network Analysis:** [NetworkX](https://networkx.org/) for modeling reply structures.
