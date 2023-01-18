from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import id_token
from google.auth.transport import requests

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            idinfo = id_token.verify_oauth2_token(token, requests.Request(),
                                                  "361303877008-ibs9vouqhtkkem140sriq8t52ims5i19.apps.googleusercontent.com")
            userid = idinfo['sub']
            print("user id is_____________", userid)

    try:

        service = build('drive', 'v3', credentials=creds)

        results = service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                       fields='files(id,name)').execute()

        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')

        for item in items:
            print(item['name'] + "-" + item['id'])

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()