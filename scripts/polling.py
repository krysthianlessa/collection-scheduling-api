from time import sleep
import requests
from requests.exceptions import ConnectionError
from decouple import config

WAIT_TIME = 60
BACKEND_URL = config("BACKEND_URL", "http://web:8000/")
LAB_ZAP_URL = config("LAB_ZAP_URL", default="http://labzap:3000/")
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

        if response.status_code == 200:
            response_data = response.json()
            return response_data["results"] if response_data["count"] > 0 else []

        # TODO: Add logs to catch when status code is not 200 OK
        return []

    def send_to_whatsapp(self, message):
        headers = {"Content-Type": "application/json"}
        payload = {
            "chatId": f"{RECIPIENT_PHONE_NUMBER}@c.us",
            "text": message,
            "session": "default"
        }
        response = requests.post(
            f"{LAB_ZAP_URL}api/sendText",
            json=payload,
            headers=headers,
        )
        print("send_to_whatsapp:", response)
        return response

    def update_schedule(self, schedule_id):
        headers = {
            "Authorization": f"Api-Key {BACKEND_API_KEY}"
        }

        response = requests.post(
            f"{BACKEND_URL}schedule/{schedule_id}/whatsapp/",
            headers=headers,
        )
        print("update_schedule:", response)


def main():
    wpp = WhatsAppIntegration()
    while True:
        schedules = wpp.get_schedules()

        for schedule in schedules:
            try:
                # E se o primeiro der OK e o segundo falhar? Vou persistir localmente tbm.
                wpp.send_to_whatsapp(schedule["whatsapp_message"])
                wpp.update_schedule(schedule["id"])
                sleep(0.3)
            except ConnectionError as connection_error:
                print("Connection Error:", connection_error)

        sleep(WAIT_TIME)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
