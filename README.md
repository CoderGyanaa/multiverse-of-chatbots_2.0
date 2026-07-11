# 🌀 The Multiverse of Chatbots

A persona-based AI chatbot built with **Python**, **Streamlit**, and the **Gemini API** — pick a personality, say something, and get a reply fully in character.

Built for **MirAI School of Technology's Virtual Summer Internship 2026** — *AI Builder Track, Assignment 2: Upgrading the AI Multiverse*.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38+-red?logo=streamlit)
![Gemini API](https://img.shields.io/badge/Gemini%20API-Free%20Tier-4285F4?logo=googlegemini)

---

## 📖 Overview

Select who you want to talk to from a dropdown of distinct personas and chat with them in a **persistent, multi-turn conversation** — powered by `st.session_state` so the history survives every rerun, persona switch, and Streamlit widget interaction. Each message is routed to the Gemini API along with the full conversation so far and a persona-specific system prompt, so the same question gets a completely different answer depending on who you ask.

---

## ✨ Features

- 🎭 **7 built-in personas** with distinct personalities (easy to add more in `utils.py`)
- 🧠 **Stateful "Memory Vault"** — `st.session_state.messages` persists the full chat history across reruns, so the app remembers earlier turns instead of wiping them on every interaction
- 💬 Native `st.chat_message` / `st.chat_input` chat UI (not a text box + button)
- ⚠️ Edge-case handling: missing API key is caught with `st.error()`
- 📜 Full conversation sent to Gemini on every turn, so replies can reference earlier messages
- 🔄 Switching personas or any sidebar control does **not** clear the chat history
- 🗑️ "Clear Conversation" button to reset the vault on demand
- 🔐 API key entered locally in the sidebar (password field) — never hardcoded or committed
- 🎨 Custom dark glassmorphism UI, styled chat bubbles

---

## 🛠 Tech Stack

| Layer      | Technology |
|------------|------------|
| Language   | Python 3.10+ |
| Framework  | Streamlit |
| AI Model   | Google Gemini API (`google-genai` SDK) |
| Styling    | Custom CSS |

---

## 🔑 Getting a Free Gemini API Key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with a Google account
3. Click **Create API Key** — no credit card required
4. Paste the key into the app's sidebar when running it

The free tier is generous enough for this app; `gemini-3.1-flash-lite` is the default since it's the cheapest, highest-quota option. `gemini-3.5-flash` is available in the dropdown for more capable (but pricier) responses.

---

## 📸 Screenshots

> Add screenshots to the `screenshots/` folder and reference them here.

| Selecting a Persona | Chatbot Response |
|----------------------|-------------------|
<img width="1918" height="892" alt="image" src="https://github.com/user-attachments/assets/68a25913-90ee-4843-9817-08404afc393e" />


---

## 📂 Folder Structure

```
multiverse-of-chatbots/
│
├── app.py              # Main Streamlit app (UI + interaction logic)
├── utils.py              # Personas + Gemini API call wrapper
├── styles.css             # Custom dark glassmorphism theme
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore               # Git ignore rules
├── assets/                   # Icons / static assets
└── screenshots/               # App screenshots for README
```

---

## 🚀 Installation

```bash
git clone https://github.com/<your-username>/multiverse-of-chatbots.git
cd multiverse-of-chatbots
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On macOS/Linux
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
streamlit run app.py
```

Paste your Gemini API key into the sidebar, pick a persona, type a message, and hit **Send**.

---

## 💻 Running in VS Code on Windows 11

1. Install [Python 3.10+](https://www.python.org/downloads/) (check "Add python.exe to PATH") and [VS Code](https://code.visualstudio.com/) with the Python extension.
2. Extract this project folder, e.g. to `C:\Projects\multiverse-of-chatbots`.
3. `File → Open Folder...` in VS Code → select the folder.
4. Open the integrated terminal (`` Ctrl+` ``) — defaults to PowerShell.
5. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
   If PowerShell blocks the script, run once: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
6. `Ctrl+Shift+P` → **"Python: Select Interpreter"** → choose `.\venv\Scripts\python.exe`
7. Install dependencies: `pip install -r requirements.txt`
8. Run the app: `streamlit run app.py`

---

## ☁️ Deployment

### Streamlit Community Cloud
1. Push this project to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
3. Click **New app**, select your repo/branch, set the main file to `app.py`.
4. Deploy. Users paste their own Gemini API key into the sidebar at runtime — no key is stored in the repo.

### Render
1. Push this project to GitHub.
2. Create a new **Web Service** on [Render](https://render.com).
3. Build command: `pip install -r requirements.txt`
4. Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

---

## ✅ Assignment Checklist (Memory Vault)

- [x] `st.session_state.messages` initialized as an empty list if not already present
- [x] `for` loop renders every past message via `st.chat_message(role)`
- [x] `st.text_input` + `st.button("SEND")` replaced with `st.chat_input("Say something...")`
- [x] Walrus operator used: `if user_message := st.chat_input(...)`
- [x] User message appended to `st.session_state.messages` as `{"role": "user", "content": ...}`
- [x] Assistant reply appended as `{"role": "assistant", "content": ...}`
- [x] Full history sent to Gemini each turn (multi-turn context, not just the latest message)
- [x] Persona dropdown change does **not** wipe the chat history
- [x] History survives 3+ message exchanges

---

## 🔮 Future Improvements

- Full multi-turn chat memory per persona (not just single-turn Q&A)
- Streaming responses token-by-token
- Custom persona builder (let users define their own system prompt)
- Voice input/output

---

### 👤 Author

Built as part of the MirAI School of Technology Virtual Summer Internship 2026 — AI Builder Track.
