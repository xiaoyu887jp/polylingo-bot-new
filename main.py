from flask import Flask, request
import requests

app = Flask(__name__)

LINE_ACCESS_TOKEN = "B3blv9hwkVhaXvm9FEpijEck8hxdiNIhhlXD9A+OZDGGYhn3mEqs71gF1i88JV/7Uh+ZM9mOBOzQlhZNZhl6vtF9X/1j3gyfiT2NxFGRS8B6I0ZTUR0J673O21pqSdIJVTk3rtvWiNkFov0BTlVpuAdB04t89/1O/w1cDnyilFU="
GOOGLE_API_KEY = "AIzaSyBOMVXr3XCeqrD6WZLRLL-51chqDA9I80o"

# 全群共用一個設定
language_settings = set()

flex_message_json = {
    "type": "bubble",
    "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [{
            "type": "text",
            "text": "🌍 Please select your translation language",
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
            {"type": "button", "style": "primary", "color": "#33CC66",
             "action": {"type": "message", "label": "🇨🇳 简体中文 (zh-cn)", "text": "/setlang_add zh-cn"}},
            {"type": "button", "style": "primary", "color": "#3399FF",
             "action": {"type": "message", "label": "🇹🇼 繁體中文 (zh-tw)", "text": "/setlang_add zh-tw"}},
            {"type": "button", "style": "primary", "color": "#FF6666",
             "action": {"type": "message", "label": "🇯🇵 日本語 (ja)", "text": "/setlang_add ja"}},
            {"type": "button", "style": "primary", "color": "#9966CC",
             "action": {"type": "message", "label": "🇰🇷 한국어 (ko)", "text": "/setlang_add ko"}},
            {"type": "button", "style": "primary", "color": "#FFCC00",
             "action": {"type": "message", "label": "🇹🇭 ภาษาไทย (th)", "text": "/setlang_add th"}},
            {"type": "button", "style": "primary", "color": "#FF9933",
             "action": {"type": "message", "label": "🇻🇳 Tiếng Việt (vi)", "text": "/setlang_add vi"}},
            {"type": "button", "style": "primary", "color": "#33CCCC",
             "action": {"type": "message", "label": "🇫🇷 Français (fr)", "text": "/setlang_add fr"}},
            {"type": "button", "style": "primary", "color": "#33CC66",
             "action": {"type": "message", "label": "🇪🇸 Español (es)", "text": "/setlang_add es"}},
            {"type": "button", "style": "primary", "color": "#3399FF",
             "action": {"type": "message", "label": "🇩🇪 Deutsch (de)", "text": "/setlang_add de"}},
            {"type": "button", "style": "primary", "color": "#4CAF50",
             "action": {"type": "message", "label": "🇮🇩 Bahasa Indonesia (id)", "text": "/setlang_add id"}},
            {"type": "button", "style": "primary", "color": "#FF6666",
             "action": {"type": "message", "label": "🇮🇳 हिन्दी (hi)", "text": "/setlang_add hi"}},
            {"type": "button", "style": "primary", "color": "#66CC66",
             "action": {"type": "message", "label": "🇮🇹 Italiano (it)", "text": "/setlang_add it"}},
            {"type": "button", "style": "primary", "color": "#FF9933",
             "action": {"type": "message", "label": "🇵🇹 Português (pt)", "text": "/setlang_add pt"}},
            {"type": "button", "style": "primary", "color": "#9966CC",
             "action": {"type": "message", "label": "🇷🇺 Русский (ru)", "text": "/setlang_add ru"}},
            {"type": "button", "style": "primary", "color": "#CC3300",
             "action": {"type": "message", "label": "🇸🇦 العربية (ar)", "text": "/setlang_add ar"}}
        ]
    }
}

def reply_to_line(reply_token, messages):
    headers = {"Authorization": f"Bearer {LINE_ACCESS_TOKEN}"}
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json={"replyToken": reply_token, "messages": messages})

def translate(text, target_lang):
    url = f"https://translation.googleapis.com/language/translate/v2?key={GOOGLE_API_KEY}"
    payload = {"q": text, "target": target_lang}
    res = requests.post(url, json=payload)
    return res.json()["data"]["translations"][0]["translatedText"]

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    for event in data["events"]:
        reply_token = event["replyToken"]
        text = event["message"]["text"]

        if text.startswith("/setlang_add"):
            lang = text.split()[1]
            language_settings.add(lang)
            reply_to_line(reply_token, [{"type": "text", "text": f"✅ Added {lang}"}])
            continue

        if not language_settings:
            reply_to_line(reply_token, [{"type": "flex", "altText": "Select language", "contents": flex_message_json}])
        else:
            translations = [{"type": "text", "text": f"[{lang.upper()}] {translate(text, lang)}"} for lang in language_settings]
            reply_to_line(reply_token, translations)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
