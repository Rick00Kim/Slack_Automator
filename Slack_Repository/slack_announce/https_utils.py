from urllib.request import urlopen
from urllib.parse import urlencode


def api_call(url, payload):

    post = urlencode(payload).encode('utf-8')

    response = urlopen(url, post)

    return response
