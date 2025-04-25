from flask import Flask, request
import requests
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# LINE & Google API Key (你的密鑰)
LINE_ACCESS_TOKEN = "B3blv9hwkVhaXvm9FEpijEck8hxdiNIhhlXD9A+OZDGGYhn3mEqs71gF1i88JV/7Uh+ZM9mOBOzQlhZNZhl6vtF9X/1j3gyfiT2NxFGRS8B6I0ZTUR0J673O21pqSdIJVTk3rtvWiNkFov0BTlVpuAdB04t89/1O/w1cDnyilFU="
GOOGLE_API_KEY = "AIzaSyBOMVXr3XCeqrD6WZLRLL-51chqDA9I80o"

# Firebase 初始化 (把你下載的JSON檔案上傳到Render，並修改為你的檔案名稱)
cred = credentials.Certificate("serviceAccountKey.json") 
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://你的專案.firebaseio.com/'
})

# Flex Message JSON (完整的語言卡片)
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
            {"type": "button", "style": "primary", "color": "#3399FF",
             "action": {"type": "message", "label": "🇯🇵 日本語 (ja)", "text": "/setlang_add ja"}},
            {"type": "button", "style": "primary", "color": "#FFCC00",
             "action": {"type": "message", "label": "🇹🇭 ภาษาไทย (th)", "text": "/setlang_add th"}}
            # 你可以依需求加上更多語言按鈕
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

# 回覆訊息函數
def reply_to_line(reply_token, messages):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {"replyToken": reply_token, "messages": messages}
    requests.post(url, headers=headers, json=payload)

# 翻譯函數
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

        user_ref = db.reference(f"/users/{user_id}")

        # 新增語言設定（永久保存）
        if text.startswith("/setlang_add"):
            lang = text.split()[1]
            langs = user_ref.get() or []
            if lang not in langs:
                langs.append(lang)
                user_ref.set(langs)
            reply_to_line(reply_token, [{"type": "text", "text": f"✅ Added {lang}"}])
            continue

        # 重置語言設定
        if text == "/resetlang":
            user_ref.delete()
            reply_to_line(reply_token, [{"type": "text", "text": "🔄 Languages reset."}])
            continue

        # 首次發言跳出卡片（從Firebase永久判斷）
        langs = user_ref.get()
        if not langs:
            reply_to_line(reply_token, [{"type": "flex", "altText": "Select languages", "contents": flex_message_json}])
            continue

        # 翻譯並回覆
        translations = []
        for lang in langs:
            translated_text = translate(text, lang)
            translations.append({"type": "text", "text": f"[{lang.upper()}] {translated_text}"})

        reply_to_line(reply_token, translations)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
