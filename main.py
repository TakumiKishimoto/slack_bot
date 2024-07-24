import os
from fastapi import FastAPI, HTTPException, Depends, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from models import SessionLocal, Command, init_db
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

app = FastAPI()
slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_client = WebClient(token=slack_token)
init_db()

# Pydanticモデル
class CommandRequest(BaseModel):
    keyword: str
    full_command: str

# データベース依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ルートエンドポイントを追加
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI is running!"}

@app.post("/commands")
async def commands(token: str = Form(...), text: str = Form(...), db: Session = Depends(get_db)):
    keyword = text.strip()
    command = db.query(Command).filter(Command.keyword == keyword).first()
    if command:
        response_text = command.full_command
    else:
        response_text = "Command not found."

    response = {
        "response_type": "in_channel",
        "text": response_text
    }
    return response

@app.post("/add_command")
async def add_command(text: str = Form(...), db: Session = Depends(get_db)):
    parts = text.split(maxsplit=1)  # 最大1回のスプリットで期待する形式に適応
    if len(parts) < 2:
        raise HTTPException(status_code=400, detail="Invalid command format. Use /addcommand keyword full_command.")
    
    keyword = parts[0]
    full_command = parts[1]
    
    command = Command(keyword=keyword, full_command=full_command)
    db.add(command)
    db.commit()
    db.refresh(command)
    return {"message": "Command added successfully"}

@app.post("/send_message")
async def send_message(channel_id: str, message: str):
    try:
        response = slack_client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        return {"message": "Message sent", "ts": response['ts']}
    except SlackApiError as e:
        raise HTTPException(status_code=500, detail=f"Error sending message: {e.response['error']}")

@app.post("/read_messages")
async def read_messages(channel_id: str, limit: int = 10):
    try:
        response = slack_client.conversations_history(
            channel=channel_id,
            limit=limit
        )
        return response['messages']
    except SlackApiError as e:
        raise HTTPException(status_code=500, detail=f"Error reading messages: {e.response['error']}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)