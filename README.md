プロジェクトを詳細に説明したREADMEファイルを以下にまとめました。このREADMEは、プロジェクトの構造、セットアップ手順、および使用方法について説明しています。

---

# Slackボット - キーワードに応じたコマンド提供

このプロジェクトは、Slackボットを開発して、特定のキーワードをSlackに投げると、事前にデータベースに格納したフルコマンドを返す機能を提供します。また、ボットに新しいコマンドを格納できるようにもなります。

## 目次
1. [環境設定と必要なライブラリのインストール](#環境設定と必要なライブラリのインストール)
2. [FastAPIアプリケーションの設定](#fastapiアプリケーションの設定)
3. [データベースモデルの定義](#データベースモデルの定義)
4. [Slackアプリケーションの設定とスコープの設定](#slackアプリケーションの設定とスコープの設定)
5. [主要エンドポイントの実装](#主要エンドポイントの実装)
6. [アプリケーションの起動とテスト](#アプリケーションの起動とテスト)
7. [構成図](#構成図)

## 環境設定と必要なライブラリのインストール

まず、プロジェクトディレクトリを作成し、必要なライブラリをインストールします。

```bash
mkdir slack_bot_project
cd slack_bot_project
python -m venv venv
source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate`
pip install fastapi uvicorn slack_sdk sqlalchemy databases python-dotenv
```

## FastAPIアプリケーションの設定

プロジェクトディレクトリに以下のファイルを作成します：`main.py`, `models.py`, `.env`

**`main.py`** (FastAPIアプリケーションのメインエントリーポイント)

```python
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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## データベースモデルの定義

**`models.py`** (データベースモデルの定義)

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True, index=True, nullable=False)
    full_command = Column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)
```

## 環境変数の設定

**`.env`** (環境変数) ファイルを作成し、以下の内容を記述します：

```plaintext
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
```

## データベースの初期化

以下のコマンドを実行してデータベースを初期化します：

```bash
python
>>> from models import init_db
>>> init_db()
```

## Slackアプリケーションの設定とスコープの設定

1. [Slack API](https://api.slack.com/) にアクセスし、「Create New App」をクリック。
2. 「From scratch」を選択。
3. アプリの名前を設定し、インストールするワークスペースを選択。
4. 「Slash Commands」を選択し、「Create New Command」をクリック。以下の情報を入力：
   - **Command:** `/your_command_here`
   - **Request URL:** `http://your-server-url/commands`
   - **Short Description:** "Triggers a custom command"
   - **Usage Hint:** `[keyword]`

5. 必要なスコープを設定（`chat:write`, `commands`, など）。
6. OAuth & Permissionsでスコープを追加し、アプリをワークスペースにインストール。
7. 得られたトークンを `.env` ファイルに保存。

## 主要エンドポイントの実装

主要なCRUD操作を提供するエンドポイント `commands` や `add_command` およびその他のユーティリティエンドポイントを設定します。

## アプリケーションの起動とテスト

ローカル環境でテストする場合、以下のコマンドを使用してアプリケーションを起動します：

```bash
uvicorn main:app --reload
```

その後、Slackのスラッシュコマンドインターフェースを使って適切にコマンドが機能することを確認します。

## 構成図

プロジェクトのディレクトリ構造は以下のようになります：

```
slack_bot_project/
│
├── main.py          : FastAPIアプリケーションのエントリーポイント
├── models.py        : データベースモデル定義
├── .env             : 環境変数ファイル（Slackトークンなど）
├── venv/            : 仮想環境ディレクトリ
└── test.db          : SQLiteデータベースファイル
```

---

このREADMEファイルを使ってプロジェクトをセットアップし、Slackボットが特定のキーワードに応じてデータベースに格納されたフルコマンドを返す機能を動かしましょう。また、新しいコマンドを追加するためのスラッシュコマンドを使って、機能を拡張することができます。