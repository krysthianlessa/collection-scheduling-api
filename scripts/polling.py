import os
from time import sleep
import requests
from decouple import config

WAIT_TIME = 60
BACKEND_URL = "http://web:8000/"
LAB_ZAP_URL = "http://labzap:3000/"
RECIPIENT_PHONE_NUMBER = config("RECIPIENT_PHONE_NUMBER", default="123")
BACKEND_API_KEY = config("BACKEND_API_KEY", default="XIYsieyz.pyysqzZIRn6GNjCxGPFjptO1nf2SA6ci")


class WhatsAppIntegration:
    def get_schedules(self):
        headers = {
            "Authorization": f"Api-Key {BACKEND_API_KEY}"
        }

        response = requests.get(
            f"{BACKEND_URL}schedule/?has_sync=0",
            headers=headers,
        )
        response_data = response.json()
        return response_data

    def send_to_whatsapp(self, message):
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

    def update_schedule(self, schedule_id):
        headers = {
            "Authorization": f"Api-Key {BACKEND_API_KEY}"
        }

        response = requests.patch(
            f"{BACKEND_URL}schedule/{schedule_id}/",
            {"has_sync": True},
            headers=headers,
        )
        response_data = response.json()
        return response_data


def main():
    wpp = WhatsAppIntegration()
    try:
        while True:
            schedules = wpp.get_schedules()

            for schedule in schedules:
                wpp.send_to_whatsapp(schedule["whatsapp_message"])
                wpp.update_schedule(schedule["id"])

            sleep(WAIT_TIME)
    except KeyboardInterrupt:
        print("Interrupted!")


if __name__ == '__main__':
    main()
