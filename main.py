from flask import Flask, request
import requests

app = Flask(__name__)

LINE_ACCESS_TOKEN = "B3blv9hwkVhaXvm9FEpijEck8hxdiNIhhlXD9A+OZDGGYhn3mEqs71gF1i88JV/7Uh+ZM9mOBOzQlhZNZhl6vtF9X/1j3gyfiT2NxFGRS8B6I0ZTUR0J673O21pqSdIJVTk3rtvWiNkFov0BTlVpuAdB04t89/1O/w1cDnyilFU="
GOOGLE_API_KEY = "AIzaSyBOMVXr3XCeqrD6WZLRLL-51chqDA9I80o"

# 用戶翻譯語言設定（支援多語）
user_language_settings = {}

# 支援 VIP 用戶（付費功能） - 手動添加 user_id
vip_users = set([
    # "Uxxxxxxxxxxxxxxxxxxxx"  ← 這裡放付費者的 LINE ID
])

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
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
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
    user_id = event["source"]["userId"]
    message = event.get("message", {})
    reply_token = event.get("replyToken")
    user_text = message.get("text", "")

    # 新語法：累加語言 /setlang_add zh-cn
    if user_text.lower().startswith("/setlang_add"):
        lang_code = user_text[13:].strip()
        current_langs = user_language_settings.get(user_id, [])
        if lang_code not in current_langs:
            current_langs.append(lang_code)
        user_language_settings[user_id] = current_langs
        reply = f"✅ 已新增語言：{lang_code.upper()}，目前翻譯語言：{', '.join(current_langs)}"
        reply_to_line(reply_token, reply)
        return "OK", 200

    # 舊語法：覆蓋語言 /setlang en,th
    if user_text.lower().startswith("/setlang"):
        lang_list = user_text[9:].split(",")
        user_language_settings[user_id] = [lang.strip() for lang in lang_list if lang.strip()]
        reply = f"✅ 語言已設定為：{', '.join(user_language_settings[user_id])}"
        reply_to_line(reply_token, reply)
        return "OK", 200

    # 一般訊息翻譯流程
    target_langs = user_language_settings.get(user_id, ["en"])
    translations = []
    for lang in target_langs:
        try:
            translated = translate(user_text, lang)
            translations.append(f"[{lang.upper()}] {translated}")
        except Exception:
            translations.append(f"[{lang.upper()}] 翻譯失敗")

    full_reply = "\n\n".join(translations)
    reply_to_line(reply_token, full_reply)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
