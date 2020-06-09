import json


def get_error_message(raw):
    return json.loads(raw.decode("utf8"))["errors"][0]["message"]
