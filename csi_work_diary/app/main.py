import json
from .member import initialize
from flask import Flask, Response, request, make_response
from slackeventsapi import SlackEventAdapter
from slack.errors import SlackApiError
from threading import Thread
from slack import WebClient
from slack.signature import SignatureVerifier
from .constants import *
from .timecard_register.register import JmottoOperator
from .member.crud import *

# This `app` represents your existing Flask app
app = Flask(__name__)

signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

# instantiating slack client
slack_client = WebClient(slack_token)

# An example of one of your Flask app's routes


@app.route("/")
def event_hook(request):
    json_dict = json.loads(request.body.decode("utf-8"))
    print(json_dict)
    if json_dict["token"] != VERIFICATION_TOKEN:
        return {"status": 403}

    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return response_dict
    return {"status": 500}


slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/slack/events", app
)


@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    def send_reply(value):
        event_data = value
        message = event_data["event"]
        if message.get("subtype") is None:
            command = message.get("text")
            channel_id = message["channel"]
            if any(item in command.lower() for item in greetings):
                message = (
                    "Hello <@%s>! :tada:"
                    % message["user"]
                )
                slack_client.chat_postMessage(channel=channel_id, text=message)
    thread = Thread(target=send_reply, kwargs={"value": event_data})
    thread.start()
    return Response(status=200)


@app.route("/slack/registDiary", methods=["POST"])
def slack_app():

    if not signature_verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("invalid request", 403)

    if "payload" in request.form:

        payload = json.loads(request.form["payload"])
        if payload["type"] == "shortcut" \
                and payload["callback_id"] == "open-modal-shortcut":
            # Open a new modal by a global shortcut
            users = select_member((payload["user"]["id"],))
            if not(users):
                try:
                    api_response = slack_client.views_open(
                        trigger_id=payload["trigger_id"],
                        view=view_new_user
                    )
                    return make_response("", 200)
                except SlackApiError as e:
                    code = e.response["error"]
                    return make_response(f"Failed to open a modal due to {code}", 200)

            try:
                api_response = slack_client.views_open(
                    trigger_id=payload["trigger_id"],
                    view=view_json
                )
                return make_response("", 200)
            except SlackApiError as e:
                code = e.response["error"]
                return make_response(f"Failed to open a modal due to {code}", 200)

        if payload["type"] == "view_submission":
            if payload["view"]["callback_id"] == "regist-modal":
                # Handle a data submission request from the modal
                submitted_data = payload["view"]["state"]["values"]
                print(submitted_data)

                input_yyyyMM = payload["view"]["state"]["values"]["date_yyyyMM"]["target_month"]["value"]
                input_password = payload["view"]["state"]["values"]["user_crenditial"]["passwd"]["value"]

                if len(input_yyyyMM) != 6:

                    validate_error = {
                        "response_action": "errors",
                        "errors": {
                            "date_yyyyMM": "Invalid date format -> please input yyyyMM"
                        }
                    }

                    return make_response(validate_error, 200)

                exists_user = select_member((payload["user"]["id"],))

                def make_register(target_date):
                    JmottoOperator(
                        (exists_user[1],
                         exists_user[2],
                         input_password),
                        (exists_user[3],
                         exists_user[4])
                    ).set_default_time_range(target_date)
                    slack_client.chat_postMessage(
                        channel=announce_channel, text="""
                        Success diary register <@{}>! \nPlease check your <https://www.j-motto.co.jp|J-MOTTO> timecard. (date -> {}) :tada:
                        """
                        .format(payload["user"]["id"],
                                input_yyyyMM
                                ))

                thr = Thread(target=make_register, args=[input_yyyyMM])
                thr.start()

                return make_response("", 200)
            if payload["view"]["callback_id"] == "regist-user":
                start_ts = payload["view"]["state"]["values"]["timeset_start"]["start_time"]["selected_option"]["value"]
                end_ts = "".join((str(int(start_ts[:2]) + 9), start_ts[2:]))
                create_member(
                    (payload["user"]["id"],
                     payload["view"]["state"]["values"]["memberID"]["jmottoMemberID"]["value"],
                     payload["view"]["state"]["values"]["UserID"]["jmottoUserID"]["value"],
                     payload["view"]["state"]["values"]["timeset_start"]["start_time"]["selected_option"]["value"],
                     end_ts))

                slack_client.chat_postMessage(
                    channel=announce_channel, text="""
                        Success default account information <@{}>! :tada:
                        """
                    .format(payload["user"]["id"],
                            ))

                return make_response("", 200)

        if payload["type"] == "block_actions" \
                and payload["actions"][0]["action_id"] == "addSpecificDate":
            print(payload["actions"][0]["action_id"])
            return make_response("", 200)

    return make_response("", 404)
