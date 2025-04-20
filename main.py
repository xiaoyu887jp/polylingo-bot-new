from flask import Flask, request
import requests

app = Flask(__name__)

# 这里请填入你的密钥（你只需要修改这里）
LINE_ACCESS_TOKEN = "bBVhlw3/hYaZ2y6QDfa0ZOgwlvAfKhz+8RU0d0LFd1H6NdtSyhekPZw3vqOnSVrBUqQmVVcJBpCB8RXkmLSnJNbd7QkZ1Gqdgnu6v5fj3x7qTiYO3luhkO4EoTQWocIeVQNxf5Z9YDtcuUlWYNPBGQdB04t89/1O/w1cDnyilFU="
GOOGLE_API_KEY = "AIzaSyBOMVXr3XCeqrD6WZLRLL-51chqDA9I80o"

user_language_settings = {}

# 完整的Flex Message JSON (确认无误✅)
flex_message_json = {
    "type": "bubble",
    "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [{
            "type": "text",
            "text": "🌍 Please choose your language",
            "weight": "bold",
            "size": "md",
            "align": "center"
        }],
        "backgroundColor": "#FFFFFF"
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": [
            {"type": "button", "style": "primary", "color": "#3B82F6",
                "action": {"type": "message", "label": "🇺🇸 English (en)", "text": "/setlang_add en"}},
            {"type": "button", "style": "primary", "color": "#22C55E",
                "action": {"type": "message", "label": "🇨🇳 简体中文 (zh-cn)", "text": "/setlang_add zh-cn"}},
            {"type": "button", "style": "primary", "color": "#FACC15",
                "action": {"type": "message", "label": "🇹🇭 ภาษาไทย (th)", "text": "/setlang_add th"}},
            {"type": "button", "style": "primary", "color": "#EF4444",
                "action": {"type": "message", "label": "🇯🇵 日本語 (ja)", "text": "/setlang_add ja"}},
            {"type": "button", "style": "primary", "color": "#8B5CF6",
                "action": {"type": "message", "label": "🇰🇷 한국어 (ko)", "text": "/setlang_add ko"}}
        ]
    }
}

# 向LINE回覆消息
def reply_to_line(reply_token, messages):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {"replyToken": reply_token, "messages": messages}
    requests.post(url, headers=headers, json=payload)

# 谷歌翻译API调用
def translate(text, target_lang):
    url = f"https://translation.googleapis.com/language/translate/v2?key={GOOGLE_API_KEY}"
    payload = {"q": text, "target": target_lang, "format": "text"}
    headers = {"Content-Type": "application/json"}
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        return res.json()["data"]["translations"][0]["translatedText"]
    else:
        return "[翻译失败]"

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    events = data.get("events", [])
    
    for event in events:
        reply_token = event["replyToken"]
        user_id = event["source"].get("userId")
        user_text = event.get("message", {}).get("text", "")
        
        if not user_id:
            continue

        # 用户选择语言
        if user_text.startswith("/setlang_add"):
            lang = user_text.split()[1]
            user_language_settings.setdefault(user_id, set()).add(lang)
            reply_to_line(reply_token, [{"type": "text", "text": f"✅ 已新增語言 {lang}"}])
            continue

        # 用户首次使用，未选择语言，发送语言选择按钮
        if user_id not in user_language_settings or len(user_language_settings[user_id]) == 0:
            reply_to_line(reply_token, [
                {"type": "flex", "altText": "Choose Language", "contents": flex_message_json}
            ])
            continue

        translations = []
        for lang in user_language_settings[user_id]:
            translated_text = translate(user_text, lang)
            translations.append({"type": "text", "text": f"[{lang.upper()}] {translated_text}"})

        reply_to_line(reply_token, translations)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
