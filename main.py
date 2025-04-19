flex_message_json = {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [{"type": "text", "text": "Language", "weight": "bold", "size": "lg", "align": "center"}],
    "backgroundColor": "#FFCC80"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "English(en)", "text": "/setlang_add en"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "繁體中文 (zh-tw)", "text": "/setlang_add zh-tw"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "简体中文 (zh-cn)", "text": "/setlang_add zh-cn"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "日本語 (ja)", "text": "/setlang_add ja"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "印尼文 (id)", "text": "/setlang_add id"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "韓文 (ko)", "text": "/setlang_add ko"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "法文 (fr)", "text": "/setlang_add fr"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "越南 (vi)", "text": "/setlang_add vi"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "泰文 (th)", "text": "/setlang_add th"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "西班牙 (es)", "text": "/setlang_add es"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "俄文 (ru)", "text": "/setlang_add ru"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "印度 (hi)", "text": "/setlang_add hi"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "葡萄牙 (pt)", "text": "/setlang_add pt"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "德文 (de)", "text": "/setlang_add de"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "阿拉伯 (ar)", "text": "/setlang_add ar"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "菲律賓 (fil)", "text": "/setlang_add fil"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "土耳其 (tr)", "text": "/setlang_add tr"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "緬甸 (my)", "text": "/setlang_add my"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "孟加拉 (bn)", "text": "/setlang_add bn"}},
      {"type": "button","style": "primary","color": "#4CAF50",
        "action": {"type": "message", "label": "柬埔寨 (km)", "text": "/setlang_add km"}}
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {"type": "button", "style": "secondary", "action": {"type": "message", "label": "重選 (reselect)", "text": "/resetlang"}}
    ]
  }
}
