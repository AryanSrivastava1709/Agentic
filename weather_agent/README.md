# 🌦️ Agentic Weather AI

A terminal-based Agentic Weather Assistant built using:

- Google Gemini API
- OpenAI Python SDK
- Python
- Pydantic
- Requests

The assistant follows a **finite-state agent architecture**, where every response progresses through well-defined phases before producing the final answer.

---

## ✨ Features

- 🌍 Current weather lookup for any city
- 🤖 Agentic workflow using finite-state architecture
- 📋 Structured JSON responses
- 🔨 Automatic tool calling
- 🧠 Pydantic structured output parsing
- 🌡️ Supports multiple city weather queries
- 🚫 Politely declines non-weather related questions
- 💬 Conversation memory using message history

---

## 🔄 Agent Workflow

The assistant follows these phases:

```
START
   ↓
PLAN
   ↓
TOOL (if required)
   ↓
OBSERVE
   ↓
OUTPUT
```

### Phase Description

| Phase   | Purpose                             |
| ------- | ----------------------------------- |
| START   | Understand the user's request       |
| PLAN    | Decide what action should be taken  |
| TOOL    | Call the required external function |
| OBSERVE | Receive tool output                 |
| OUTPUT  | Generate the final response         |

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Agentic.git
cd weather_agent
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

### 5. Run the application

```bash
python main.py
```

---

## 🛠️ Tech Stack

- Python
- Google Gemini API
- OpenAI Python SDK
- Pydantic
- Requests
- python-dotenv

---

## 📁 Project Structure

```
Agentic-Weather-AI/
│
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Available Tool

### `get_weather(city)`

Fetches the current weather for a city using **wttr.in**.

Example:

```
Input:
Delhi

Output:
The weather in Delhi is Partly cloudy and the temperature is +34°C
```

---

## 📷 Preview

```text
Please enter your query 👉 What's the weather in Delhi?

🔥 The user wants to know the current weather in Delhi.

🤯 I need to fetch the current weather using the available tool.

🔨 get_weather Delhi

🟰 The weather in Delhi is Partly cloudy and the temperature is +34°C
```

---

## 🧠 Example Workflow

**User**

```
What's the weather in Tokyo?
```

↓

**START**

```
Understand the user's request.
```

↓

**PLAN**

```
Determine that weather information requires an external tool.
```

↓

**TOOL**

```
get_weather("Tokyo")
```

↓

**OBSERVE**

```
The weather in Tokyo is Sunny and the temperature is +29°C
```

↓

**OUTPUT**

```
The weather in Tokyo is Sunny and the temperature is +29°C.
```

---

## 📌 Notes

- Every model response is validated using **Pydantic**.
- The assistant always returns structured JSON internally.
- Only one phase is executed per model response.
- Tool execution happens outside the LLM and is fed back through an `OBSERVE` step.
- Non-weather queries are politely declined without invoking the planning or tool phases.

---
