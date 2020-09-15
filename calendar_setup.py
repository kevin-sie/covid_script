import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'credentials.json'


def get_calendar_service():
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the
    # authorization flow completes for the first time
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def create_event(res):
    service = get_calendar_service()
    res = res.split()
    res[0] = res[0].split('/')
    res[1] = res[1].split(':')
    print(res)
    res_time = datetime.datetime(int(res[0][2]), int(res[0][0]), int(res[0][1]), int(res[1][0]) + 12, int(res[1][1]))
    end_time = datetime.datetime(int(res[0][2]), int(res[0][0]), int(res[0][1]), int(res[1][0]) + 13, 0)

    event = {
        'summary': 'covid test',
        'start': {
            'dateTime': res_time.isoformat(),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/New_York',
        },
    }

    event = service.events().insert(calendarId='kevinsie1899@gmail.com', body=event).execute()
    print("event created")
