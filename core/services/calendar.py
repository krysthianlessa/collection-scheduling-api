from google.oauth2 import service_account
from googleapiclient.discovery import build

from core.models import Schedule

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
        if create:
            return api_service.events().insert(calendar_id=calendar_id, body=event)
        else:
            return api_service.events().update(calendar_id=calendar_id, event_id=schedule.calendar_event_id, body=event)