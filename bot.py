from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from models import db, Command

app = Flask(__name__)
slack_token = "xoxb-5921280756961-5894677219223-wywKj8SCzouEUU65F0JHbZc2"
slack_client = WebClient(token=slack_token)

if __name__ == '__main__':
    app.run(debug=True)

# スラッシュコマンドのエンドポイント
@app.route('/commands', methods=['POST'])
def commands():
    data = request.json
    if data['type'] == 'slash_commands':
        keyword = data['text'].strip()
        command = Command.query.filter_by(keyword=keyword).first()
        if command:
            response_text = command.full_command
        else:
            response_text = "Command not found."

        response = {
            "response_type": "in_channel",
            "text": response_text
        }
        return jsonify(response)
    return jsonify({"message": "Invalid request"})

@app.route('/add_command', methods=['POST'])
def add_command():
    data = request.json
    keyword = data.get('keyword')
    full_command = data.get('full_command')

    if keyword and full_command:
        command = Command(keyword=keyword, full_command=full_command)
        db.session.add(command)
        db.session.commit()
        return jsonify({"message": "Command added successfully"})
    else:
        return jsonify({"message": "Invalid data"})