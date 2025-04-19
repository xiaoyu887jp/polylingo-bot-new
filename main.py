from flask import Flask, request
import requests

app = Flask(__name__)

LINE_ACCESS_TOKEN = "B3blv9hwkVhaXvm9FEpijEck8hxdiNIhhlXD9A+OZDGGYhn3mEqs71gF1i88JV/7Uh+ZM9mOBOzQlhZNZhl6vtF9X/1j3gyfiT2NxFGRS8B6I0ZTUR0J673O21pqSdIJVTk3rtvWiNkFov0BTlVpuAdB04t89/1O/w1cDnyilFU="
GOOGLE_API_KEY = "AIzaSyBOMVXr3XCeqrD6WZLRLL-51chqDA9I80o"
user_language_settings = {}

# Flex 語言選擇卡片JSON (你設計的按鈕圖)
flex_message_json = {
  "type": "flex",
  "altText": "選擇你要的翻譯語言",
  "contents": {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {"type": "text", "text": "選擇語言 Choose language", "weight": "bold", "size": "md"},
        {"type": "button", "action": {"type": "message", "label": "English", "text": "/setlang_add en"}},
        {"type": "button", "action": {"type": "message", "label": "ภาษาไทย", "text": "/setlang_add th"}},
        {"type": "button", "action": {"type": "message", "label": "日本語", "text": "/setlang_add ja"}},
        {"type": "button", "action": {"type": "message", "label": "重新選擇 (Reset)", "text": "/resetlang"}}
      ]
    }
  }
}

def reply_to_line(reply_token, messages):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {"replyToken": reply_token, "messages": messages}
    requests.post(url, headers=headers, json=payload)

def detect_language(text):
    url = f"https://translation.googleapis.com/language/translate/v2/detect?key={GOOGLE_API_KEY}"
    res = requests.post(url, json={"q": text})
    return res.json()["data"]["detections"][0][0]["language"]

def translate(text, target_lang):
    url = f"https://translation.googleapis.com/language/translate/v2?key={GOOGLE_API_KEY}"
    res = requests.post(url, json={"q": text, "target": target_lang})
    return res.json()["data"]["translations"][0]["translatedText"]

@app.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    events = data.get("events", [])
    for event in events:
        reply_token = event["replyToken"]
        user_id = event["source"]["userId"]

        # 加好友或加入群組 → 自動跳出Flex語言選單圖片
        if event["type"] == "follow" or event["type"] == "join":
            reply_to_line(reply_token, [flex_message_json])
            continue

        user_text = event.get("message", {}).get("text", "")
        if user_text.startswith("/setlang_add"):
            lang = user_text.split()[1]
            user_language_settings.setdefault(user_id, set()).add(lang)
            reply_to_line(reply_token, [{"type": "text", "text": f"✅ 語言已設定為 {lang}"}])
            continue

        if user_text == "/resetlang":
            user_language_settings[user_id] = set()
            reply_to_line(reply_token, [{"type": "text", "text": "✅ 語言設定已清空，請重新選擇。"}])
            continue

        target_langs = user_language_settings.get(user_id, [])
        if not target_langs:
            reply_to_line(reply_token, [{"type": "text", "text": "你還沒設定語言，請先點按鈕設定語言。"}])
            continue

        # 語言已選 → 自動翻譯
        translated_messages = []
        for lang in target_langs:
            translation = translate(user_text, lang)
            translated_messages.append({"type": "text", "text": f"[{lang.upper()}] {translation}"})

        reply_to_line(reply_token, translated_messages)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
