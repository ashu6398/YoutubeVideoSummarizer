# 🎬 LLM YouTube Video Summarizer

A FastAPI-based web app that allows users to summarize YouTube videos using [Whisper](https://github.com/openai/whisper) for audio transcription and [Gemini](https://ai.google.dev/) for summarization. 

This project automates the process of downloading the video's audio, transcribing it to text, and generating a concise, chapter-style summary using a powerful LLM.

---

## 🚀 Features

- 🔗 Accepts YouTube video URLs
- 🧠 Transcribes audio using OpenAI Whisper
- ✨ Summarizes text with Gemini 2.0 Flash
- 📄 Displays final summary on the UI
- 🎯 Simple and responsive web UI built with FastAPI + Jinja2

---

## 🖼️ Final Output


![image](https://github.com/user-attachments/assets/08e7808a-80fe-40de-a1a0-3ce5d8819c50)

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/youtube-video-summarizer.git
cd youtube-video-summarizer
```

### 2. Create & activate Conda environment
```bash
conda create -n YoutubeSummarizer python=3.10
conda activate YoutubeSummarizer
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

Make sure `ffmpeg` is installed and placed in the correct folder (e.g. `/ffmpeg/bin` in project root).

---

## 🔑 Set Up Google API Key

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=your_google_gemini_api_key
```

---

## ▶️ Run the App

```bash
python.exe app.py
```

Then open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📁 Project Structure

```
youtube-video-summarizer/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── ffmpeg/
│   └── bin/
├── requirements.txt
└── .env
```

---

## 🛠️ Tech Stack

- Python, FastAPI
- Jinja2 Templates
- OpenAI Whisper
- Google Gemini API
- yt-dlp for YouTube audio download
- ffmpeg for audio processing

---

## 📌 To Do

- [ ] Add support for language detection
- [ ] Add download option for summaries
- [ ] Add LLM selector (Gemini / GPT / Claude)

---

## 📃 License

This project is licensed under the MIT License.

---

⭐ If you like this project, give it a star on GitHub and share it!
