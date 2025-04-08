from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_event(summary, description, start_time, duration_minutes=30):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    start = start_time.isoformat()
    end = (start_time + datetime.timedelta(minutes=duration_minutes)).isoformat()

    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start, 'timeZone': 'Europe/Paris'},
        'end': {'dateTime': end, 'timeZone': 'Europe/Paris'},
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return f"✅ Événement créé : {event_result['htmlLink']}"
