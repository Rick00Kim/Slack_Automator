import os

slack_token = os.environ.get('SLACK_OAUTH_TOKEN')
slack_channel = '#api_test_room'
slack_post_message_url = 'https://slack.com/api/chat.postMessage'
slack_get_userid_by_email = 'https://slack.com/api/users.lookupByEmail'

attachment_color_success = '#b2fab4'
attachment_color_warn = '#ff6161'

module_dict = {}
