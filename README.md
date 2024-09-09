
# Slackボット - キーワードに応じたコマンド提供

このプロジェクトは、Slackボットを利用して、特定のキーワードに応じたコマンドをSlackチャット内で提供する機能を持っています。また、ボットに新しいコマンドを追加したり、既存のコマンドを削除することもできます。

## 目次
1. [機能概要](#機能概要)
2. [環境設定とインストール](#環境設定とインストール)
3. [使い方](#使い方)
4. [主要エンドポイントの説明](#主要エンドポイントの説明)
5. [Slack APIの設定](#slack-apiの設定)
6. [ローカルでのテスト](#ローカルでのテスト)
7. [RenderへのデプロイとSlack設定](#renderへのデプロイとslack設定)


## 機能概要

- **コマンド取得**: Slackで指定したキーワードに関連するフルコマンドを取得できます。
- **すべてのコマンドの取得**: データベースに保存されたすべてのコマンドを取得し、一覧表示できます。
- **コマンドの追加**: 新しいコマンドをデータベースに追加できます。
- **コマンドの削除**: 既存のコマンドをデータベースから削除できます。

## 環境設定とインストール

1. このリポジトリをクローンします。

    ```bash
    git clone https://github.com/TakumiKishimoto/slack_bot.git
    cd slack_bot
    ```

2. Poetryを使って依存関係をインストールします。

    ```bash
    poetry install
    ```

3. 次に、Slack APIの設定を行い、発行されたトークンを`.env` ファイルに書き込みます。

## Slack APIの設定

1. **Slackアプリの作成**:
   - [Slack API](https://api.slack.com/) にアクセスして、ログイン後「Your Apps」から「Create New App」をクリックします。
   - 「From scratch」を選択し、アプリ名とインストールするワークスペースを指定します。
   
2. **OAuth & Permissions**:
   - 左側のメニューから「OAuth & Permissions」を選択し、**Bot Token Scopes**セクションで以下のスコープを追加します。
     - `commands`: Slashコマンドを使用するために必要です。
     - `chat:write`: ボットがメッセージを送信するために必要です。
   - スコープ追加後、「Install to Workspace」をクリックしてワークスペースにインストールし、発行された**ボットトークン**をコピーします。

3. **Slash Commands の作成**:
   - 左側のメニューから「Slash Commands」を選択し、「Create New Command」をクリックします。
   - コマンド情報を入力します:
     - **Command**: 使用するコマンド名（例: `/command`）
     - **Request URL**: デプロイしたアプリケーションのエンドポイント（例: `https://your-app-name.onrender.com/command`）
     - **Short Description**: コマンドの説明
     - **Usage Hint**: コマンドの使い方のヒント（例: `/command keyword`）

4. **環境変数ファイルにトークンを設定**:
   - Slack APIから取得したボットトークンを使い、`.env` ファイルに以下のように書き込みます。

    ```plaintext
    SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
    ```
## ローカルでのテスト

1. **ローカルサーバーの起動**:
   - 以下のコマンドを実行して、ローカルサーバーを起動します。

    ```bash
    poetry run python main.py
    ```

2. **テストコードの実行**:
   - プロジェクトには、Slackボットの機能をテストするための簡単なテストスクリプトが含まれています。以下のコマンドでテストを実行できます。

    ```bash
    poetry run python tests/add_commands.py
    ```

   - このテストスクリプトは、ローカルサーバーでのコマンドの追加、取得、削除が正しく動作するかを確認します。

3. **テスト結果の確認**:
   ![実行結果の様子](img/local_test2.png)
   ![実行結果の様子](img/local_test1.png)
   
   - これで、Slackボットの使用が可能になり、コマンドを実行した際に応答が返されるようになります。ローカルでのテストにより、実際の環境にデプロイする前に機能が正常に動作するか確認できます。

## RenderへのデプロイとSlack設定

1. **Renderへのデプロイ**:
   - Renderのアカウントにログインし、新しいウェブサービスを作成します。
   - GitHubリポジトリからこのプロジェクトを選択し、サービスをデプロイします。
   - デプロイ後、Renderから提供されるURLをコピーしておきます。

2. **Slack設定の更新**:
   - 先ほど取得したRenderのURLをSlackの「Slash Commands」設定に貼り付け、Slackとアプリケーションの連携を有効にします。




---