# 🎥 YouTube Transcript AI Agent

![App Demo](./Youtube-Transcript-AI-Agent.gif)

A premium, modern web interface that transforms any YouTube video into actionable AI-powered insights in seconds. Built with a focus on "Cinema Scholar" aesthetics and real-time streaming analysis.

![GitHub last commit](https://img.shields.io/github/last-commit/balamurugan-shanmuganathan/Google-Adk-Projects)
![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)

---

## ✨ Features

- **Real-Time Streaming**: AI analysis flows directly to the screen via Server-Sent Events (SSE).
- **Cinema Aesthetic**: Premium dark-mode interface with glassmorphism, glowing accents, and smooth animations.
- **Dynamic 2-Column Dashboard**: View the embedded video and the AI summary side-by-side.
- **Markdown Rendering**: High-quality formatted output including headers, bold points, and lists.
- **Instant Embedding**: Automatic video preview generation from any valid YouTube URL.
- **Fully Responsive**: Optimized for desktop and mobile viewing.

---

## 🛠️ Tech Stack

- **Core**: [Google ADK](https://github.com/google/adk) (Agent Development Kit)
- **AI Model**: Gemini 2.0 Flash Lite via `google-genai`
- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Markdown Engine**: Showdown.js

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- A Google Gemini API Key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/balamurugan-shanmuganathan/Google-Adk-Projects.git
   cd Google-Adk-Projects/YouTube-Transcript-AI-Agent
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**:
   Ensure your environment is set up with your Google API credentials or configured via the ADK.

---

## 🖱️ Usage

1. **Start the UI Server**:
   ```bash
   python3 server.py
   ```
2. **Open the Application**:
   Navigate to [http://localhost:8001](http://localhost:8001) in your browser.
3. **Analyze**:
   Paste any YouTube URL into the input field and hit "Analyze Video."

---

## 📂 Project Structure

```text
YouTube-Transcript-AI-Agent/
├── ui/                  # Web Interface assets
│   ├── index.html       # Main HTML structure
│   ├── style.css        # Premium Design System
│   └── app.js           # Real-time streaming & Logic
├── youtube_transcript_ai_agent/
│   ├── agent.py         # Google ADK Agent definition
│   └── tools/           # Custom tools (Transcript fetching)
├── server.py            # FastAPI UI & SSE Server
├── main.py              # CLI Entry point
└── requirements.txt     # Python dependencies
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

**Created by [Bala Murugan](https://github.com/balamurugan-shanmuganathan)**
