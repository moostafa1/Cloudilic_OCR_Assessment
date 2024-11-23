from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from config import CONFIG
import io
import os
import time

# Google Drive API settings
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = "1Q2LQ-WpybQWhASauytf89YKnSdNHkDDG"  # Replace with your folder ID
CREDENTIALS_FILE = CONFIG["credentials_path"]  # Path to your OAuth 2.0 credentials JSON

def authenticate():
    """Authenticate using OAuth 2.0 and return the service instance."""
    creds = None

    # Check if token.json exists to reuse credentials
    if os.path.exists(CONFIG["token_path"]):
        creds = Credentials.from_authorized_user_file(CONFIG["token_path"], SCOPES)

    # Refresh or re-authenticate if necessary
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8000)

        # Save the credentials for future use
        with open(CONFIG["token_path"], 'w') as token_file:
            token_file.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def monitor_folder():
    """Monitor the designated folder for new files."""
    service = authenticate()

    # Fetch initial state of the folder
    response = service.files().list(
        q=f"'{FOLDER_ID}' in parents and trashed = false",
        spaces='drive',
        fields='files(id, name)',
    ).execute()

    seen_files = {file['id']: file['name'] for file in response.get('files', [])}

    print("Monitoring folder for changes...")
    while True:
        # Fetch current state of the folder
        response = service.files().list(
            q=f"'{FOLDER_ID}' in parents and trashed = false",
            spaces='drive',
            fields='files(id, name)',
        ).execute()

        current_files = {file['id']: file['name'] for file in response.get('files', [])}

        # Identify new files
        new_files = {id_: name for id_, name in current_files.items() if id_ not in seen_files}

        for file_id, file_name in new_files.items():
            print(f"New file detected: {file_name}")
            download_file(service, file_id, file_name)

        # Update seen files
        seen_files = current_files

        # Wait before polling again
        time.sleep(10)  # Adjust polling interval as needed

def download_file(service, file_id, file_name):
    """Download a file from Google Drive."""
    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join(CONFIG["invoices_save_dir"], file_name)  # Save to 'downloads' folder

    # Ensure the downloads folder exists
    os.makedirs(CONFIG["invoices_save_dir"], exist_ok=True)

    with open(file_path, 'wb') as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")

    print(f"File '{file_name}' downloaded successfully to {file_path}")

if __name__ == "__main__":
    monitor_folder()
