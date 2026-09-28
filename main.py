import os
import requests
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# GitHub Secrets से टोकन्स उठाना
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GMAIL_USER = os.environ.get("GMAIL_USER")          
GMAIL_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD") 

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_telegram_message(chat_id, text):
    """टेलीग्राम पर मैसेज भेजने के लिए"""
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

def check_telegram_updates():
    """टेलीग्राम से नया कमांड चेक करने के लिए"""
    url = f"{BASE_URL}/getUpdates"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results = data.get("result", [])
            if results:
                latest_update = results[-1]
                message = latest_update.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text", "")
                return chat_id, text
    except Exception as e:
        print(f"Telegram Fetch Error: {e}")
    return None, None

def check_latest_email():
    """जीमेल इनबॉक्स से सबसे नया अनरेड ईमेल पढ़ने के लिए"""
    if not GMAIL_USER or not GMAIL_PASSWORD:
        return "Gmail credentials not set in GitHub Secrets."
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASSWORD)
        mail.select("inbox")
        
        status, messages = mail.search(None, 'UNSEEN')
        if status != 'OK':
            return "कोई नया अनरेड ईमेल नहीं मिला।"
            
        email_ids = messages[0].split()
        if not email_ids:
            return "इनबॉक्स में कोई नया ईमेल नहीं है।"
            
        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg["Subject"]
                sender = msg["From"]
                return f"📩 नया ईमेल मिला!\nFrom: {sender}\nSubject: {subject}"
        
        mail.logout()
    except Exception as e:
        return f"Gmail Read Error: {str(e)}"
    return "ईमेल चेक करने में कोई डेटा नहीं मिला।"

def main():
    print("🤖 Super AI Agent Engine running...")
    chat_id, text = check_telegram_updates()
    
    if chat_id and text:
        print(f"Command received: {text}")
        text_lower = text.lower()
        
        if "youtube" in text_lower:
            reply = "🇺🇸 US YouTube Agent: वायरल वीडियो आइडिया और स्क्रिप्ट तैयार हो रही है!"
        elif "game" in text_lower or "app" in text_lower:
            reply = "🎮 App/Game Agent: गेम का कोड लिखकर GitHub Pages पर डिप्लॉय किया जा रहा है..."
        elif "email" in text_lower or "mail" in text_lower:
            email_status = check_latest_email()
            reply = f"📧 Gmail Agent Status:\n{email_status}"
        else:
            reply = f"✅ सुपर एजेंट एक्टिव है! आपका कमांड मिला: '{text}'"
        
        send_telegram_message(chat_id, reply)
    else:
        print("No new commands. Standing by.")

if __name__ == "__main__":
    main()
