import os
import os.path
import pyodbc
import datetime
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

server = 'CS_T0511'
database = 'ecom_backend'
username = ''
password = ''

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/docs',
          'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', ]

recent_file = None
del_filename = None
folder_id = None
temp = '1'
recent_files = []
data_files = []

while True:
    print(recent_files)


    def get_backup():
        import datetime
        current_time = datetime.datetime.now()

        timee = str(current_time.timestamp()).split('.')

        str_current_datetime = timee[0]
        file_name = str_current_datetime + ".bak"

        cxnn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cxnn.autocommit = True
        connection = cxnn.cursor()
        f = open(file_name, "a")
        f.close()
        backup = f"BACKUP DATABASE [ecom_backend] TO DISK = 'C:\hardik\projects\demo\gmailapi\{file_name}'"
        data_files.append(file_name)
        print(backup)
        cursor = connection.execute(backup)
        connection.close()
        return None


    def main():

        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials_drive.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            global folder_id
            global del_filename
            global recent_file

            service = build('drive', 'v3', credentials=creds)
            if folder_id is None:
                file_metadata = {
                    'name': 'backUp3',
                    'mimeType': 'application/vnd.google-apps.folder'
                }

                file = service.files().create(body=file_metadata, fields='id'
                                              ).execute()
                folder_id = file.get('id')
                print(folder_id)
            get_backup()
            current_datetime = datetime.now()

            str_current_datetime = str(current_datetime)
            file_metadata = {
                'name': str_current_datetime,
                'parents': [f'{folder_id}']
            }
            media = MediaFileUpload('Mydatabase.bak',
                                    mimetype='application/octet-stream', resumable=True)
            file = service.files().create(body=file_metadata, media_body=media,
                                          fields='id').execute()
            newfile_id = file.get('id')

            if len(recent_files) == 3:
                idd = recent_files[0]
                file = service.files().delete(fileId=idd).execute()
                recent_files.pop(0)
                remove = data_files[0]
                os.remove(remove)
                data_files.pop(0)

                del_filename = newfile_id
            recent_files.append(newfile_id)

            # if del_filename is not None:

        except HttpError as error:
            print(f'An error occurred: {error}')


    if __name__ == '__main__':
        main()
    # time.sleep(30)
