import json
import os

with open("app/message_format/app_view.json", "r") as fmt_view:
    view_json = json.load(fmt_view)
    fmt_view.close()

with open("app/message_format/new_user.json", "r") as fmt_new_user:
    view_new_user = json.load(fmt_new_user)
    fmt_new_user.close()

SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
slack_token = os.environ['SLACK_BOT_TOKEN']
VERIFICATION_TOKEN = os.environ['VERIFICATION_TOKEN']

announce_channel = "auto_register_timecard"

greetings = ["hi", "hello", "hello there", "hey"]

function_diary = ["diary", "타임카드 등록"]

# J-MOTTO constants
login_url = 'https://www1.j-motto.co.jp/fw/dfw/po80/portal/contents/login.html'

time_card_main_url = 'https://gws51.j-motto.co.jp/cgi-bin/{}/ztcard.cgi?cmd=tcardindex#date={}&cmd=tcardindex'

time_card_register_url = 'https://gws51.j-motto.co.jp/cgi-bin/{}/ztcard.cgi?cmd=tcardindex#cmd=tcardentry&id={}'
