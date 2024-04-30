import requests
from core.models import Schedule
from django.conf import settings


class WhatsAppService:
    url = "https://labzap.onrender.com/api/sendText"

    @classmethod
    def send_message(cls, message_body: str):
        payload = {
            "chatId": f"{settings.RECIPIENT_PHONE_NUMBER}@c.us",
            "text": "Hi there!\nThis is a test.",
            "session": "default"
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            settings.LAB_ZAP_URL,
            json=payload,
            headers=headers,
        )

        print(response.text)
