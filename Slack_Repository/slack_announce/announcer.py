import json
from .https_utils import api_call
from .constants import *


with open("slack_announce/msg_format/report_format.json", "r") as summary:
    post_json = json.load(summary)

with open("slack_announce/msg_format/attachment_format.json", "r") as attachment:
    post_attachment = json.load(attachment)


def count_severity(measure_data, target_severity):
    return sum(map(lambda x: x['severity'] ==
                   target_severity, measure_data['issues']))


def get_userid_by_email(email):

    post = {
        "token": slack_token,
        "email": email
    }

    response = api_call(slack_get_userid_by_email, post)

    result_json = json.loads(response.readline().decode('utf8'))

    if result_json['ok'] == True:
        return result_json['user']['id']
    else:
        return None


def post_message(project_key, measure_data):

    announce_target = get_userid_by_email('dreamx119@gmail.com')

    if announce_target:
        post_json[0]['text']['text'] = " <@{0}>".format(announce_target)
    else:
        post_json[0]['text']['text'] = "<!here>"

    post_json[1]['fields'][0]['text'] = "Test String"

    post_attachment['title'] = project_key
    post_attachment['fields'][0]['value'] = measure_data['total']
    post_attachment['fields'][1]['value'] = count_severity(
        measure_data, 'CRITICAL')
    post_attachment['fields'][2]['value'] = count_severity(
        measure_data, 'BLOCKER')

    post = {
        "token": slack_token,
        "channel": slack_channel,
        "text": "Sonar Report Result",
        "blocks": json.dumps([post_json[0], post_json[1]]),
        "attachments": json.dumps([post_attachment])
    }

    api_call(slack_post_message_url, post)
