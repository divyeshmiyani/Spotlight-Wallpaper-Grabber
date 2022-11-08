# Saves Wallpaper/s to Google Drive
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

folder_id = 0


class SaveToGoogleDrive:
    def __init__(self):
        with open("data.json") as jsonfile:
            self.data = json.load(jsonfile)

        SCOPES = ['https://www.googleapis.com/auth/drive']

        self.creds = None

        try:
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            self.creds.refresh(Request())
        except:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            self.creds = flow.run_local_server(port=0)
        finally:
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        # google drive folder metadata
        self.folder_metadata = {
            'name': 'Spotlight Wallpaper',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        self.service = build('drive', 'v3', credentials=self.creds, static_discovery=False)

    def __del__(self):
        with open('data.json', 'w') as fp:
            json.dump(self.data, fp)

    def __search_folder(self):
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

    def __is_already_uploaded(self, file_name):
        return file_name in self.data['filesUploaded']

    def __upload_file(self, path):
        file_name = path.split('\\')[-1] + '.jpg'

        if self.__is_already_uploaded(file_name):
            return

        metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(path, mimetype='image/jpeg')
        self.service.files().create(body=metadata, media_body=media, fields='id').execute()
        self.data['filesUploaded'].append(file_name)

    def execute(self, path):
        global folder_id
        if not folder_id:
            folder_id = self.__search_folder()
        self.__upload_file(path)
