from time import sleep
from random import uniform
from datetime import datetime
import requests
from requests.exceptions import ConnectionError
from decouple import config
from soonerdb import SoonerDB

WAIT_TIME = 60
BACKEND_URL = config("BACKEND_URL", "http://web:8000/")
LAB_ZAP_URL = config("LAB_ZAP_URL", default="http://labzap:3000/")
RECIPIENT_PHONE_NUMBER = config("RECIPIENT_PHONE_NUMBER", default="123")
BACKEND_API_KEY = config("BACKEND_API_KEY", default="XIYsieyz.pyysqzZIRn6GNjCxGPFjptO1nf2SA6ci")


class WhatsAppIntegration:
    labzap_headers = {"Content-Type": "application/json"}

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
        
        payload = {
            "chatId": f"{RECIPIENT_PHONE_NUMBER}@c.us",
            "text": message,
            "session": "default"
        }

        print("payload:", payload)
        response = requests.post(
            f"{LAB_ZAP_URL}api/sendText",
            json=payload,
            headers=self.labzap_headers,
        )
        print("send_to_whatsapp:", response, response.content)
        return response.status_code == 201

    def update_schedule(self, schedule_id):
        headers = {
            "Authorization": f"Api-Key {BACKEND_API_KEY}"
        }

        response = requests.post(
            f"{BACKEND_URL}schedule/{schedule_id}/whatsapp/",
            headers=headers,
        )
        print("update_schedule:", response)

    def is_session_active(self):
        response = requests.get(
            f"{LAB_ZAP_URL}api/sessions/",
            headers=self.labzap_headers,
        )
        print("Is session active:", response, ",", response.content)
        return (response.status_code == 200 and len(response.json()) > 0 and response.json()[0]["status"] == "WORKING")

    def start_session(self):
        response = requests.post(
            f"{LAB_ZAP_URL}api/sessions/start",
            json={"name": "default"},
            headers=self.labzap_headers,
        )
        print("start Session:", response)

def nightly():
    now = datetime.now()
    # período noturno entre 22 e 6 da manhã
    return now.hour <= 6 or now.hour >= 22

def little_wait(start = 0):
    """Sleep one moment"""
    value = start + uniform(0.2, 0.6)
    sleep(value)

def main():
    print("Polling started at", datetime.now())
    local_db = SoonerDB("./db")
    wpp = WhatsAppIntegration()
    # logged = db.get(today, None)
    # db.set(today, "LOG_TODAY")

    while True:
        little_wait(WAIT_TIME)

        if nightly():
            continue

        if not wpp.is_session_active():
            little_wait()
            wpp.start_session()
            little_wait(10)

        little_wait()
        for schedule in wpp.get_schedules():
            try:
                # TODO: E se o primeiro der OK e o segundo falhar? Vou persistir localmente tbm.
                if wpp.send_to_whatsapp(schedule["whatsapp_message"]):
                    wpp.update_schedule(schedule["id"])

                little_wait()
            except ConnectionError as connection_error:
                print("Connection Error:", connection_error)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
