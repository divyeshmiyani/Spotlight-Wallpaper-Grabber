# Saves Wallpaper/s to Google Drive
import json
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

folder_id = 0


class SaveToGoogleDrive:
    def __init__(self):
        print('__init__')
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/drive']

        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.folder_metadata = {
            'name': 'SpotlightWallpaper',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        self.service = build('drive', 'v3', credentials=self.creds, static_discovery=False)

    def __search_folder(self):
        print('search folder')
        # Page Token
        page_token = None

        while True:
            # Call the Drive v3 API
            results = self.service.files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                fields="nextPageToken, files(id, name)",
                                                pageToken=page_token).execute()
            items = results.get('files', [])
            page_token = results.get('nextPageToken', None)

            for item in items:
                if item.get('name') == self.folder_metadata['name']:
                    return item.get('id')
            if page_token is None:
                file = self.service.files().create(body=self.folder_metadata, fields='id').execute()
                return file.get('id')

    @staticmethod
    def __is_already_uploaded(file_name):
        print('is already present')
        with open("data.json") as jsonfile:
            data = json.load(jsonfile)

        if file_name in data['filesUploaded']:
            return True

        data['filesUploaded'].append(file_name)

        print(data['filesUploaded'])
        with open('data.json', 'w') as fp:
            json.dump(data, fp)

    def __upload_file(self, path):
        print('upload file')
        file_name = path.split('\\')[-1] + '.jpg'

        if self.__is_already_uploaded(file_name):
            return

        metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(path, mimetype='image/jpeg')
        self.service.files().create(body=metadata, media_body=media, fields='id').execute()
        print('uploaded file')

    def execute(self, path):
        print('execute')
        global folder_id
        if not folder_id:
            folder_id = self.__search_folder()
        self.__upload_file(path)
