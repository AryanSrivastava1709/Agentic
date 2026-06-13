# 🎮 GameGuru

A terminal-based AI-powered PC Gaming chatbot built using:

- Google Gemini API
- OpenAI Python SDK
- Rich
- Python

---

## ✨ Features

- 🎮 PC game recommendations
- 🎯 Mood-based suggestions
- ⚔️ Boss fight help
- 🧩 Gameplay explanations
- 💻 Hardware-based recommendations
- 💬 Conversation memory

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/GameGuru.git
cd GameGuru
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a file named `.env` in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
```

You can get a Gemini API key from **Google AI Studio**.

### 5. Run the chatbot

```bash
python main.py
```

---

## 🛠️ Tech Stack

- Python
- Google Gemini API
- OpenAI Python SDK
- Rich
- python-dotenv

---

## 📷 Preview

```
🎮 GameGuru

🎯 You: Recommend some horror games

╭──────────── 🎮 GameGuru ────────────╮
│ • Resident Evil Village             │
│ • Dead Space Remake                 │
│ • Alien Isolation                   │
│ • Outlast                           │
╰─────────────────────────────────────╯

⚡ Response Time: 1.82s
```
