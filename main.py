from flask import Flask, request
import requests

app = Flask(__name__)

LINE_ACCESS_TOKEN = "B3blv9hwkVhaXvm9FEpijEck8hxdiNIhhlXD9A+OZDGGYhn3mEqs71gF1i88JV/7Uh+ZM9mOBOzQlhZNZhl6vtF9X/1j3gyfiT2NxFGRS8B6I0ZTUR0J673O21pqSdIJVTk3rtvWiNkFov0BTlVpuAdB04t89/1O/w1cDnyilFU="
GOOGLE_API_KEY = "AIzaSyBOMVXr3XCeqrD6WZLRLL-51chqDA9I80o"

user_language_settings = {}

def detect_language(text):
    url = f"https://translation.googleapis.com/language/translate/v2/detect?key={GOOGLE_API_KEY}"
    payload = {"q": text}
    headers = {"Content-Type": "application/json"}
    res = requests.post(url, json=payload, headers=headers, timeout=5)
    res.raise_for_status()
    return res.json()["data"]["detections"][0][0]["language"]

def translate(text, target_lang):
    url = f"https://translation.googleapis.com/language/translate/v2?key={GOOGLE_API_KEY}"
    payload = {"q": text, "target": target_lang, "format": "text"}
    headers = {"Content-Type": "application/json"}
    res = requests.post(url, json=payload, headers=headers, timeout=5)
    res.raise_for_status()
    return res.json()["data"]["translations"][0]["translatedText"]

def reply_to_line(reply_token, message):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(url, headers=headers, json=payload)

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    events = data.get("events", [])
    if not events:
        return "OK", 200

    event = events[0]
    message = event.get("message", {})
    reply_token = event.get("replyToken")
    user_id = event["source"]["userId"]
    user_text = message.get("text", "")

    if user_text.lower().startswith('/setlang'):
        lang = user_text.split(' ')[1].lower()
        user_language_settings[user_id] = lang
        reply_to_line(reply_token, f"语言已设置为 {lang}")
        return "OK", 200

    source_lang = detect_language(user_text)
    target_lang = user_language_settings.get(user_id, "en")

    translated_text = translate(user_text, target_lang)
    reply_to_line(reply_token, translated_text)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
