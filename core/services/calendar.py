from google.oauth2 import service_account
from googleapiclient.discovery import build
from core.models import Schedule, ScheduleCalendarIntegration


class CalendarService():

    @classmethod
    def create_api_service(cls):
        service_account_file = "service_account_file.json"
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        return build('calendar', 'v3', credentials=credentials)

    @classmethod
    def sync_to_google_api(cls, schedule: Schedule, create = True):
        api_service = cls.create_api_service()
        calendar_id = schedule.shared_calendar.filter().first
        event = {
            'summary': schedule.full_name,
            'description': schedule.event_description,
            'start': {
                'dateTime': schedule.start,
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': schedule.end,
                'timeZone': 'America/Sao_Paulo',
            },
        }

        service_event = api_service.events()
        params = {
            "calendar_id": calendar_id,
            "body": event,
        }

        if create:
            event_data = service_event.insert(**params)
        else:
            event_data = service_event.update(**params, event_id=schedule.calendar_event_id)

        ScheduleCalendarIntegration.objects.create(
            schedule=schedule,
            data=event_data,
        )
