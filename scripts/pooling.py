import os
from time import sleep
import requests

WAIT_TIME = 60
BACKEND_URL = ""
LAB_ZAP_URL = "http://labzap:3000/"
RECIPIENT_PHONE_NUMBER = os.environ.get("RECIPIENT_PHONE_NUMBER", default="123")
BACKEND_API_KEY = os.environ.get("BACKEND_API_KEY", default="XIYsieyz.pyysqzZIRn6GNjCxGPFjptO1nf2SA6ci")


def get_schedules():
    headers = {
        "Authorization": f"Api-Key {BACKEND_API_KEY}"
    }

    response = requests.get(
        f"{BACKEND_URL}/schedule/?has_sync=0",
        headers=headers,
    )
    response_data = response.json()
    return response_data


def send_to_whatsapp(message):
    headers = {"Content-Type": "application/json"}
    payload = {
        "chatId": f"{RECIPIENT_PHONE_NUMBER}@c.us",
        "text": message,
        "session": "default"
    }
    response = requests.post(
        f"{LAB_ZAP_URL}/api/sendText",
        json=payload,
        headers=headers,
    )
    return response

def update_schedule(schedule_id):
    headers = {
        "Authorization": f"Api-Key {BACKEND_API_KEY}"
    }

    response = requests.patch(
        f"{BACKEND_URL}/schedule/{schedule_id}/",
        {"has_sync": True},
        headers=headers,
    )
    response_data = response.json()
    return response_data


def main():
    try:
        while True:
            schedules = get_schedules()
            for schedule in schedules:
                send_to_whatsapp(schedule["message"])

                update_schedule(schedule["id"])

            sleep(WAIT_TIME)
    except KeyboardInterrupt:
        print("Interrupted!")


if __name__ == '__main__':
    main()
