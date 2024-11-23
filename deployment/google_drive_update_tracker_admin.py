from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from config import CONFIG
import io

# Set up scopes and folder ID
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = "1Q2LQ-WpybQWhASauytf89YKnSdNHkDDG"


def authenticate():
    creds = Credentials.from_service_account_file(
        CONFIG["service_account_path"], scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)


def monitor_folder():
    """Monitor a designated folder for changes."""
    service = authenticate()

    # Get the initial state of the folder
    response = service.files().list(
        q=f"'{FOLDER_ID}' in parents and trashed = false",
        spaces='drive',
        fields='files(id, name)',
    ).execute()

    # Maintain a list of already seen files
    seen_files = {file['id']: file['name'] for file in response.get('files', [])}

    print("Monitoring for changes...")
    while True:
        # Fetch the current state of the folder
        response = service.files().list(
            q=f"'{FOLDER_ID}' in parents and trashed = false",
            spaces='drive',
            fields='files(id, name)',
        ).execute()

        current_files = {file['id']: file['name'] for file in response.get('files', [])}
        
        # Detect new files
        new_files = {id_: name for id_, name in current_files.items() if id_ not in seen_files}

        for file_id, file_name in new_files.items():
            print(f"New file detected: {file_name}")
            download_file(service, file_id, file_name)

        # Update the seen files
        seen_files = current_files

def download_file(service, file_id, file_name):
    """Download a file from Google Drive."""
    request = service.files().get_media(fileId=file_id)
    file_path = f"{CONFIG['invoices_save_dir']}/{file_name}"  # Save to the 'downloads' folder

    with open(file_path, 'wb') as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")

    print(f"File {file_name} downloaded successfully to {file_path}")

if __name__ == "__main__":
    monitor_folder()