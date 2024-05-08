from google.oauth2 import service_account
from googleapiclient.discovery import build
from core.models import Schedule, ScheduleCalendarIntegration


class CalendarService():

    @classmethod
    def create_api_service(cls):
        service_account_file = "service_account_key.json"
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
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

        if schedule.calendar_event_id is None:
            event_data = service_event.insert(**params).execute()
        else:
            event_data = service_event.update(**params, eventId=schedule.calendar_event_id).execute()

        ScheduleCalendarIntegration.objects.create(
            schedule=schedule,
            data=event_data,
        )
        Schedule.objects.filter(id=schedule.id).update(calendar_event_id=event_data["id"])
