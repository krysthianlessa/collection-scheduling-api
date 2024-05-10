import base64
import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from core.models import Schedule, ScheduleCalendarIntegration
from django.conf import settings
import logging

logger = logging.getLogger('default')


class CalendarService():

    @staticmethod
    def _get_json_path():
        path = Path(settings.BASE_DIR, "service_account_key.json")

        if os.path.isfile(path):
            return path

        service_account_key_b64 = settings.SERVICE_ACCOUNT_KEY
        service_account_key = base64.b64decode(service_account_key_b64.encode("utf-8"))
        service_account_key_utf8 = service_account_key.decode("utf-8")
        service_account_key_normalized = service_account_key_utf8

        with open(path, "w") as file:
            file.write(service_account_key_normalized)

        return path

    @classmethod
    def create_api_service(cls):
        credentials = service_account.Credentials.from_service_account_file(
            cls._get_json_path(),
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        return build('calendar', 'v3', credentials=credentials)

    @classmethod
    def sync_to_google_api(cls, schedule: Schedule):
        api_service = cls.create_api_service()
        calendar_id = schedule.shared_calendar.identify
        event = {
            'summary': schedule.full_name,
            'description': schedule.event_description,
            'start': {
                'dateTime': schedule.start.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': schedule.end.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'America/Sao_Paulo',
            },
        }

        service_event = api_service.events()
        params = {
            "calendarId": calendar_id,
            "body": event,
        }

        try:
            if schedule.calendar_event_id is None:
                logger.info("service_event.insert %s", calendar_id, exc_info=1)
                event_data = service_event.insert(**params).execute()
            else:
                logger.info("service_event.update %s", calendar_id, exc_info=1)
                event_data = service_event.update(**params, eventId=schedule.calendar_event_id).execute()
        except Exception as error:
            logger.warning("Error when try sync with google calendar %s", error, exc_info=1)
        else:
            ScheduleCalendarIntegration.objects.create(
                schedule=schedule,
                data=event_data,
            )
            Schedule.objects.filter(id=schedule.id).update(calendar_event_id=event_data["id"])
