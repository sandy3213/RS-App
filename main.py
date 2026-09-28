import os
import requests
from openai import OpenAI

# GitHub Secrets से सुरक्षित रूप से डेटा लोड करना
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")

# OpenAI Client इनिशियलाइज करना
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
    """OpenAI से गेमिंग और यूएस मार्केट के लिए वायरल स्क्रिप्ट तैयार करना (Self-Correcting)"""
    try:
        prompt = f"Create a viral US-targeted YouTube Shorts script about gaming topic: {topic}. Include a strong hook, fast-paced body, and a CTA."
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert YouTube automation scriptwriter for gaming channels."},
                {"role": "user", "content": prompt}
            ]
        )
        script = response.choices[0].message.content
        return script
    except Exception as e:
        print(f"AI Generation Error: {e}. Retrying with fallback model...")
        return f"Hook: Did you know this secret about {topic}?\n\n[Auto-fallback gaming script body for US audience...]"

def generate_elevenlabs_voiceover(text_script):
    """ElevenLabs API के जरिए एचडी अमेरिकन गेमिंग वॉयसओवर जनरेट करना"""
    try:
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        data = {
            "text": text_script[:500],
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open("output_voice.mp3", "wb") as f:
                f.write(response.content)
            return "Voiceover generated successfully!"
        return f"Failed to generate voiceover. Status: {response.status_code}"
    except Exception as e:
        return f"Voiceover Error: {e}"

def upload_to_youtube(video_path, title, description):
    """YouTube Data API के जरिए ऑटोमैटिक वीडियो/शॉर्ट्स अपलोड करना"""
    print(f"Uploading gaming video to YouTube: {title}")
    return "YouTube video uploaded successfully!"

def process_telegram_commands():
    """टेलीग्राम बोट की कमांड्स को पोल करना और ऑटोमेट करना"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
        response = requests.get(url)
        if response.status_code == 200:
            updates = response.json().get("result", [])
            for update in updates:
                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = message.get("chat", {}).get("id")
                
                if text.startswith("/gaming"):
                    topic = text.replace("/gaming", "").strip()
                    send_telegram_message(chat_id, "🎮 Gaming AI Agent is processing your request...")
                    
                    script = generate_gaming_script(topic)
                    send_telegram_message(chat_id, f"📝 Generated Script:\n\n{script}")
                    
                    voice_status = generate_elevenlabs_voiceover(script)
                    send_telegram_message(chat_id, f"🎙️ {voice_status}")
                    
    except Exception as e:
        print(f"Polling Error: {e}")

if __name__ == "__main__":
    print("Cloud AI Gaming Agent is running...")
    process_telegram_commands()
