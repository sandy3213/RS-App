import os
import requests
from openai import OpenAI
from moviepy.editor import VideoFileClip, AudioFileClip

# GitHub Secrets से सुरक्षित रूप से डेटा उठाना
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

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
    """OpenAI से गेमिंग और शॉर्ट्स के लिए वायरल स्क्रिप्ट तैयार करना"""
    try:
        prompt = f"Create a viral US-targeted YouTube Shorts script about gaming topic: {topic}. Keep it engaging with a strong hook."
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert Youtube automation scriptwriter for gaming channels."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return f"Hook: Did you know this crazy secret about {topic}? Watch till the end!"

def generate_elevenlabs_voiceover(text_script):
    """ElevenLabs API के जरिए वॉइसओवर जनरेट करना"""
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
                
                vid_response = requests.get(video_url)
                if vid_response.status_code == 200:
                    with open("background_footage.mp4", "wb") as f:
                        f.write(vid_response.content)
                    return True
        return False
    except Exception as e:
        print(f"Pexels Error: {e}")
        return False

def create_final_video():
    """MoviePy के जरिए वीडियो और ऑडियो को आपस में मर्ज करके फाइनल वीडियो बनाना"""
    try:
        # ऑडियो लोड करना ताकि उसकी लंबाई पता चल सके
        audio_clip = AudioFileClip("output_voice.mp3")
        duration = audio_clip.duration

        # वीडियो फुटेज लोड करना
        video_clip = VideoFileClip("background_footage.mp4")
        
        # अगर वीडियो छोटा है तो लूप करना, बड़ा है तो ऑडियो की लंबाई के बराबर ट्रिम करना
        if video_clip.duration < duration:
            video_clip = video_clip.loop(duration=duration)
        else:
            video_clip = video_clip.subclip(0, duration)

        # वीडियो में ऑडियो सेट करना
        final_clip = video_clip.set_audio(audio_clip)
        
        # फाइनल वीडियो को रेंडर करके सेव करना
        final_clip.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
        
        # मेमोरी फ्री करने के लिए क्लिप्स बंद करना
        audio_clip.close()
        video_clip.close()
        final_clip.close()
        return True
    except Exception as e:
        print(f"MoviePy Rendering Error: {e}")
        return False

def process_telegram_commands():
    """टेलीग्राम कमांड्स को प्रोसेस करना और वीडियो बनाने की पूरी प्रक्रिया चलाना"""
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
                    send_telegram_message(chat_id, "🚀 AI Agent is processing your request...")
                    
                    # 1. स्क्रिप्ट जनरेट करना
                    script = generate_gaming_script(topic)
                    send_telegram_message(chat_id, f"📝 Script Generated:\n{script}")
                    
                    # 2. वॉइसओवर बनाना
                    if generate_elevenlabs_voiceover(script):
                        send_telegram_message(chat_id, "🎙️ Voiceover generated successfully!")
                    else:
                        send_telegram_message(chat_id, "❌ Voiceover generation failed.")
                        continue
                        
                    # 3. पिक्सल्स से फुटेज डाउनलोड करना
                    if download_pexels_footage(topic if topic else "gaming"):
                        send_telegram_message(chat_id, "🎬 Background footage downloaded!")
                    else:
                        send_telegram_message(chat_id, "❌ Footage download failed.")
                        continue
                        
                    # 4. MoviePy से वीडियो रेंडर करना
                    send_telegram_message(chat_id, "⚙️ Rendering final video using MoviePy...")
                    if create_final_video():
                        send_telegram_message(chat_id, "✅ Success! Final Video Generated (`final_video.mp4`). Ready for upload.")
                    else:
                        send_telegram_message(chat_id, "❌ Video rendering failed.")
    except Exception as e:
        print(f"Polling Error: {e}")

if __name__ == "__main__":
    process_telegram_commands()
