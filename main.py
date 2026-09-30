import os
import requests
import time
from openai import OpenAI
from moviepy.editor import VideoFileClip, AudioFileClip

# GitHub secrets से सुरक्षित रूप से डेटा उठाना
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

# OpenAI Client initialization करना
client = OpenAI(api_key=OPENAI_API_KEY)

def send_telegram_message(chat_id, text):
    """टेलीग्राम पर मैसेज भेजने का फंक्शन"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

def generate_gaming_script(topic):
    """OpenAI से स्क्रिप्ट और वीडियो के लिए prompt तैयार किया जाएगा"""
    try:
        prompt = f"Create a viral US-targeted YouTube Shorts script about {topic}."
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert Youtube scriptwriter."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return f"Hook: Did you know this crazy secret about {topic}? Wait until the end..."

def generate_elevenlabs_voiceover(text_script):
    """ElevenLabs API के जरिए वॉइसओवर तैयार करना"""
    try:
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        data = {
            "text": text_script,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open("output_voice.mp3", "wb") as f:
                f.write(response.content)
            return True
        return False
    except Exception as e:
        print(f"Voiceover Error: {e}")
        return False

def download_pexels_footage(query="gaming gameplay"):
    """Pexels API से फ्री गेमिंग वीडियो फुटेज डाउनलोड करना"""
    try:
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1"
        headers = {"Authorization": PEXELS_API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            videos = data.get("videos", [])
            if videos:
                video_files = videos[0].get("video_files", [])
                best_file = max(video_files, key=lambda x: x.get("width", 0))
                video_url = best_file.get("link")
                
                vid_data = requests.get(video_url)
                with open("background_video.mp4", "wb") as f:
                    f.write(vid_data.content)
                return True
        return False
    except Exception as e:
        print(f"Pexels Error: {e}")
        return False

if __name__ == "__main__":
    print("Bot is ready and running...")
    while True:
        time.sleep(60)
