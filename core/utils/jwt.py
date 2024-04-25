from django.contrib.auth.models import User


def jwt_create_response_payload(token: str, user: User = None, request=None, issued_at=None):
    shared_calendar = user.shared_calendar.filter(is_active=True).first()
    data = {
        "token": token,
        "username": user.username,
    }

    if shared_calendar is not None:
        data["sector"] = shared_calendar.sector,
        data["neighborhood"] = shared_calendar.neighborhood,

    return data
