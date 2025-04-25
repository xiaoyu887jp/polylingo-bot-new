from flask import Flask, request
import requests

app = Flask(__name__)

LINE_ACCESS_TOKEN = "bBVhlw3/hYaZ2y6QDfa0ZOgwlvAfKhz+8RU0d0LFd1H6NdtSyhekPZw3vqOnSVrBUqQmVVcJBpCB8RXkmLSnJNbd7QkZ1Gqdgnu6v5fj3x7qTiYO3luhkO4EoTQWocIeVQNxf5Z9YDtcuUlWYNPBGQdB04t89/1O/w1cDnyilFU="
GOOGLE_API_KEY = "AIzaSyBOMVXr3XCeqrD6WZLRLL-51chqDA9I80o"

user_language_settings = {}

# 完整的Flex Message JSON (16種語言)
flex_message_json = {
    "type": "bubble",
    "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [{
            "type": "text",
            "text":  "🌍 Please select your translation language",
            "weight": "bold",
            "size": "lg",
            "align": "center"
        }],
        "backgroundColor": "#FFCC80"
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {"type": "button", "style": "primary", "color": "#4CAF50",
             "action": {"type": "message", "label": "🇺🇸 English (en)", "text": "/setlang_add en"}},
            {"type": "button", "style": "primary", "color": "#3399FF",
             "action": {"type": "message", "label": "🇯🇵 日本語 (ja)", "text": "/setlang_add ja"}},
            {"type": "button", "style": "primary", "color": "#FFCC00",
             "action": {"type": "message", "label": "🇹🇭 ภาษาไทย (th)", "text": "/setlang_add th"}}
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "button", "style": "secondary",
             "action": {"type": "message", "label": "🔄 Reset", "text": "/resetlang"}}
        ]
    }
}

def reply_to_line(reply_token, messages):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
    payload = {"replyToken": reply_token, "messages": messages}
    requests.post(url, headers=headers, json=payload)

def translate(text, target_lang):
    url = f"https://translation.googleapis.com/language/translate/v2?key={GOOGLE_API_KEY}"
    payload = {"q": text, "target": target_lang, "format": "text"}
    res = requests.post(url, json=payload)
    return res.json()["data"]["translations"][0]["translatedText"]

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    for event in data.get("events", []):
        reply_token = event["replyToken"]
        user_id = event["source"].get("userId")
        text = event.get("message", {}).get("text", "")

        if text.startswith("/setlang_add"):
            lang = text.split()[1]
            if user_id not in user_language_settings:
                user_language_settings[user_id] = set()
            user_language_settings[user_id].add(lang)
            reply_to_line(reply_token, [{"type": "text", "text": f"✅ Added {lang}"}])
            continue

        if text == "/resetlang":
            user_language_settings[user_id] = set()
            reply_to_line(reply_token, [{"type": "text", "text": "🔄 Languages reset."}])
            continue

        langs = user_language_settings.get(user_id)
        if not langs:
            reply_to_line(reply_token, [{"type": "flex", "altText": "Select languages", "contents": flex_message_json}])
            continue

        translations = [{"type": "text", "text": f"[{l.upper()}] {translate(text, l)}"} for l in langs]
        reply_to_line(reply_token, translations)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
