# Puzzle Game - Voice Recognition Edition

### 🎯 Project Background

“Turtle Soup” is a type of situational riddle game. Typically played in groups, one person hosts the riddle while others ask questions, which can only be answered with “Yes” or “No.” The riddle is solved when a player can accurately reconstruct the scenario in the host’s mind, especially clarifying the initially confusing aspects.

### 🎮 Gameplay

A scene description is given, and players ask questions using **voice input**. The system recognizes speech and calls the **ChatGPT API** to answer questions, helping players reason out the real scenario.

### ✨ Project Highlights

- Beautiful and intuitive game interface
- User-friendly interaction via mouse, keyboard, and voice
- AI-powered question answering
- Innovative and potential commercial value

### 🛠️ Technologies

- **Flask** framework for web development, with a lightweight **SQLite** database for data management
- **ChatGPT API** for dynamic question answering
- **iFlyTek API** for speech-to-text conversion

### 🖼️ Game Screenshots

1. **Welcome Screen** – Click anywhere to start:

   ![welcome](./image/welcome.png)
   
2. **Theme Selection** – Choose a theme:

   ![menu](./image/menu.png)
   
   Hovering shows detailed theme info:
   
   ![menu1](./image/menu1.png)
   
3. **Theme Details** – Learn rules, how to ask questions, guess the answer, interact with the “soup surface,” and access the Q&A interface:

   ![detail](./image/detail.png)
   
4. **Q&A Interaction** – Click “Start Recording” to ask questions by voice. ChatGPT responds with “Yes” or “No”:

   ![detail1](./image/detail1.png)
   
5. **View Answer** – Click “Show Answer” to see if your guess matches the correct solution:

   ![result](./image/result.png)

------

## ⚙️ Usage

1. **Clone the repository:**

```
git clone <repository_url>
cd puzzle
```

2. **Set up your ChatGPT API key**

   You need to apply for a ChatGPT API key from OpenAI.

3. **Install dependencies**

4. **Run the Flask server:**

```
python app.py
```

5. **Open the game in your browser:**

```
http://localhost:5000
```
