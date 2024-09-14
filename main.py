# main.py
import userstatus
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime

app = Flask(__name__)

# Your Bot User OAuth Token
slack_token = "xoxb-"
client = WebClient(token=slack_token)

@app.route('/')
def hello_world():
    current_datetime = datetime.now()
    f"Hello, World! The current date and time is: {current_datetime}"
    return f"Hello, World Shilpa! The current date and time is: {current_datetime}"

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    print(data)
    # Handle the URL verification challenge from Slack
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    if "event" in data:
        event_type = data["event"]["type"]
        if event_type == "message" and not "bot_id" in data["event"]:
            channel_id = data["event"]["channel"]
            user = data["event"]["user"]
            text = data["event"]["text"]
            if text == "Hi" or text =="Hello":
                channel_id = "C01F228D8BH"
                action = userstatus.list_members_info(channel_id)
            else:
                action="logoff"


            try:
                response = client.chat_postMessage(
                    channel=channel_id,
                    text=f"Hello <@{user}>! \n You said: {text} \n Welcome Back \n {action} "
                )

            except SlackApiError as e:
                print(f"Error sending message: {e.response['error']}")

    return jsonify({"status": "Hello <@>! \n You said:  \n Welcome Back \n"}), 200

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5001, debug = True)
