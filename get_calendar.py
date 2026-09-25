import sys
import os
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "auth"))
from google_auth import get_calendar_service


def get_calendar(days: int = 7):
    """
    List upcoming events from the user's primary Google Calendar,
    for the next `days` days (default 7).
    """
    service = get_calendar_service()

    now = datetime.datetime.utcnow().isoformat() + "Z"
    later = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat() + "Z"

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        timeMax=later,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = events_result.get("items", [])

    if not events:
        return f"No events found in the next {days} days."

    return [
        {
            "summary": event.get("summary", "No title"),
            "start": event["start"].get("dateTime", event["start"].get("date")),
        }
        for event in events
    ]