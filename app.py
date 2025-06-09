from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
import uvicorn
import yt_dlp  # Used to download YouTube videos
import whisper  # Used to transcribe audio to text
from google import genai  # Used to call Gemini model for summarization

# Set up the path to ffmpeg (used for processing audio)
ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg", "bin")
os.environ["PATH"] += os.pathsep + ffmpeg_dir

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")  # Get Gemini API key

# Function to extract and transcribe audio from a YouTube URL
def getTextFromURL(youtube_url):
    try:
        # yt_dlp options to download and convert YouTube video to mp3
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': ffmpeg_dir,
            'outtmpl': 'temp_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
        }
        # Download the video audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        audio_file = "temp_audio.mp3"
        if not os.path.exists(audio_file):
            raise Exception("Audio file not downloaded")

        # Load Whisper model and transcribe the audio
        whisper_model = whisper.load_model("base")
        result = whisper_model.transcribe(audio_file)
        return result["text"]  # Return the transcribed text

    except Exception as e:
        print(f"❌ Error downloading or processing video: {e}")
        raise

# Function to summarize transcript using Gemini API
def summarize_with_gemini(transcript):
    client = genai.Client(api_key=api_key)  # Authenticate with Gemini
    prompt = (
        "You are an AI assistant. Summarize the following YouTube transcript clearly. "
        "Break it into chapters if possible. Keep it short but informative. Transcript:"
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt + transcript
    )
    return response.text  

# Initialize the FastAPI application
app = FastAPI()

# Set up static files and template directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Handle GET request to the home page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Handle POST request to /summarize when user submits a YouTube URL
@app.post("/summarize", response_class=HTMLResponse)
async def summarize(request: Request, youtube_url: str = Form(...)):
    result = getTextFromURL(youtube_url)
    summary = summarize_with_gemini(result)
    return templates.TemplateResponse("index.html", {"request": request, "summary": summary})

# Run the FastAPI server if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)