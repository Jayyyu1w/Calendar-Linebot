import os
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class Google_Calendar:
    def __init__(self):
        self.creds = None
        self.service = None
        self.service = None
        self.get_creds()
        self.get_service()
    
    def get_creds(self):
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
    
    def get_service(self):
        self.service = build("calendar", "v3", credentials=self.creds)

    def convert_time_to_rfc3339(self, date_time_str):
        dt_iso = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M").isoformat()
        return dt_iso

    def add_event(self, event):
        event["purpose"] = list(event["purpose"])
        for time_range in event["time"]:
            calendar_event = {
                'summary': event["purpose"][0],
                'location': event["location"][0],
                'start': {
                    'dateTime': self.convert_time_to_rfc3339(time_range[0]),
                    'timeZone': 'Asia/Taipei',
                },
                'end': {
                    'dateTime': self.convert_time_to_rfc3339(time_range[1]),
                    'timeZone': 'Asia/Taipei',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            insert_event_result = self.service.events().insert(calendarId='primary', body=calendar_event).execute()
            print('Event created: %s' % (insert_event_result.get('htmlLink')))