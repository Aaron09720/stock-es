"""Line notify."""
import requests

NOTIFY_TOKEN = 'pmgKo6PXIbyye4aUz12cvqwjkv80jseJaDXiVb3L9kB'


def send_notify_msg(msg: str):
    """send notify msg."""
    headers = {
        "Authorization": f"Bearer {NOTIFY_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "message": f"\n{msg}"
    }

    requests.post("https://notify-api.line.me/api/notify", headers=headers, params=params)
