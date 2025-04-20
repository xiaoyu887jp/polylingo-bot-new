from flask import Flask, request
import requests

app = Flask(__name__)

LINE_ACCESS_TOKEN = "bBVhlw3/hYaZ2y6QDfa0ZOgwlvAfKhz+8RU0d0LFd1H6NdtSyhekPZw3vqOnSVrBUqQmVVcJBpCB8RXkmLSnJNbd7QkZ1Gqdgnu6v5fj3x7qTiYO3luhkO4EoTQWocIeVQNxf5Z9YDtcuUlWYNPBGQdB04t89/1O/w1cDnyilFU="
GOOGLE_API_KEY = "AIzaSyBOMVXr3XCeqrD6WZLRLL-51chqDA9I80o"

user_language_settings = {}

flex_message_json = {
    "type": "bubble",
    "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [{"type": "text", "text": "🌍 Language", "weight": "bold", "size": "lg", "align": "center"}],
        "backgroundColor": "#FFCC80"
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {"type": "button", "style": "primary", "color": "#4CAF50", "action": {"type": "message", "label": "🇺🇸 English (en)", "text": "/setlang_add en"}},
            {"type": "button", "style": "primary", "color": "#33CC66", "action": {"type": "message", "label": "🇨🇳 简体中文 (zh-cn)", "text": "/setlang_add zh-cn"}},
            {"type": "button", "style": "primary", "color": "#3399FF", "action": {"type": "message", "label": "🇹🇼 繁體中文 (zh-tw)", "text": "/setlang_add zh-tw"}},
            {"type": "button", "style": "primary", "color": "#FF6666", "action": {"type": "message", "label": "🇯🇵 日本語 (ja)", "text": "/setlang_add ja"}},
            {"type": "button", "style": "primary", "color": "#9966CC", "action": {"type": "message", "label": "🇰🇷 한국어 (ko)", "text": "/setlang_add ko"}},
            {"type": "button", "style": "primary", "color": "#FFCC00", "action": {"type": "message", "label": "🇹🇭 ภาษาไทย (th)", "text": "/setlang_add th"}}
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "button", "style": "secondary", "action": {"type": "message", "label": "🔄 重新選擇 (Reset)", "text": "/resetlang"}}
        ]
    }
}

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

def translate(text, target_lang):
    url = f"https://translation.googleapis.com/language/translate/v2?key={GOOGLE_API_KEY}"
    payload = {"q": text, "target": target_lang, "format": "text"}
    headers = {"Content-Type": "application/json"}
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=5)
        res.raise_for_status()
        return res.json()["data"]["translations"][0]["translatedText"]
    except Exception as e:
        return f"[Translation Failed]: {e}"

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    events = data.get("events", [])
    if not events:
        return "OK", 200

    event = events[0]
    message = event.get("message", {})
    reply_token = event.get("replyToken")
    user_id = event["source"].get("userId")
    user_text = message.get("text", "")

    if user_text.startswith("/setlang_add"):
        lang = user_text.split()[1]
        user_language_settings.setdefault(user_id, set()).add(lang)
        reply_to_line(reply_token, f"✅ 已新增語言 {lang}")
        return "OK", 200

    if user_text == "/resetlang":
        user_language_settings[user_id] = set()
        reply_to_line(reply_token, "🔄 语言已重置，请重新选择。")
        return "OK", 200

    target_langs = user_language_settings.get(user_id, [])
    if not target_langs:
        reply_to_line(reply_token, "🌍 請先選擇語言 (Choose languages first)")
        return "OK", 200

    translations = []
    for lang in target_langs:
        translated_text = translate(user_text, lang)
        translations.append(f"[{lang.upper()}] {translated_text}")

    reply = "\n\n".join(translations)
    reply_to_line(reply_token, reply)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
