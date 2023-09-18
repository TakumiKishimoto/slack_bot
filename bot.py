import os
import sqlite3
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from flask import Flask, request, jsonify

# Slack APIトークンを環境変数から取得します
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# Flaskアプリケーションを初期化します
app = Flask(__name__)

# Slack APIクライアントを初期化します
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Slack Event Adapterを初期化します
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# SQLiteデータベースに接続
def get_db_connection():
    conn = sqlite3.connect("my_database.db")
    return conn

# スラッシュコマンドのエンドポイントを設定します
@app.route("/slack/command", methods=["POST"])
def handle_command():
    # スラッシュコマンドのリクエストを受け取ります
    command_text = request.form.get("text")

    if command_text.startswith("add "):
        # 語句とキーワードをデータベースに追加
        parts = command_text[4:].split(" ")
        if len(parts) >= 2:
            keyword = parts[0]
            phrase = " ".join(parts[1:])
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO phrases (keyword, phrase) VALUES (?, ?)", (keyword, phrase))
            conn.commit()
            conn.close()
            response_text = f"キーワード '{keyword}' に語句 '{phrase}' が登録されました。"
        else:
            response_text = "キーワードと語句を指定してください。"
    elif command_text.startswith("list "):
        # キーワードに対応する語句をデータベースから取得
        keyword = command_text[5:]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT phrase FROM phrases WHERE keyword=?", (keyword,))
        phrases = [row[0] for row in cursor.fetchall()]
        conn.close()
        if phrases:
            response_text = f"{keyword} の登録語句: " + ", ".join(phrases)
        else:
            response_text = f"{keyword} には登録語句がありません。"
    else:
        response_text = "不明なコマンドです"

    # Slackに応答を送信します
    response = slack_client.chat_postMessage(
        channel=request.form["channel_id"],
        text=response_text
    )

    return "", 200

if __name__ == "__main__":
    app.run(debug=True)
