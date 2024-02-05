from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load the service account credentials from the JSON key file
credentials = service_account.Credentials.from_service_account_file(
    "secret/drive_key.json",
    scopes=['https://www.googleapis.com/auth/drive']
)

# Create a Google Drive API service
drive_service = build('drive', 'v3', credentials=credentials)


def get_folder_member_emails(folderId):
    load_dotenv("secret/.env")
    members_ignore_list = os.getenv('emails_to_ignore').split(',')


    results = drive_service.permissions().list(fileId=folderId, fields="permissions(emailAddress)").execute()
    permissions = results.get('permissions', [])


    member_emails =[]
    for perm in permissions:
        if perm['emailAddress'] in members_ignore_list:
            continue
        member_emails.append(perm['emailAddress'].lower())
        #print(perm['emailAddress'])

    print("Current Member Count: ", len(member_emails))
    return member_emails



def list_files(drive_service):
    results = drive_service.files().list(fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print('No files found in Google Drive.')
    else:
        print('Files in Google Drive:')

    for file in files:
        print(f"File Name: {file['name']}, File ID: {file['id']}")




def add_drive_member(member_email, folder_id):
    print("GRANT ACCESS TO EMAIL:", member_email)

    # Load service account credentials
    key_path = 'secret/drive_key.json'

    credentials = service_account.Credentials.from_service_account_file(key_path, scopes=['https://www.googleapis.com/auth/drive'])


    # Create Google Drive API service
    drive_service = build('drive', 'v3', credentials=credentials)


    permission = {
        'type': 'user',
        'role': 'reader',  # Adjust the role as needed (reader, writer, commenter, organizer, owner)
        'emailAddress': member_email
    }

    try:
        # Add the member to the Google Drive folder
        drive_service.permissions().create(fileId=folder_id, body=permission, sendNotificationEmail=False,
                                           supportsAllDrives=True).execute()
        print("accessing drive data")
        return f"Member '{member_email}' added to the folder with ID '{folder_id}'"

    except Exception as e:
        print(f"An error occurred: {str(e)}")








def remove_members(members_to_remove, folderId):
    fields = 'permissions(id,emailAddress)'
    response2 = drive_service.permissions().list(fileId=folderId, fields=fields).execute()
    id_dict = {}
    for permission in response2.get('permissions', []):
        id_dict[permission['emailAddress']] = permission['id']

    print("ID DICT")
    print(id_dict) #{email: id, ...}
    match_list =[]
    for member in members_to_remove:
        if member in id_dict:
            match_list.append(member)

    print("FOUND USERS TO REMOVE:")
    print(match_list)
    print("USERS TO REMOVE COUNT: ", len(match_list))
    print("CONFIRM")
    to_remove = input("y/n")
    if to_remove == 'y':
        for member in match_list:
            drive_service.permissions().delete(fileId=folderId, permissionId=id_dict[member]).execute()
            print("REMOVED ", member)
        return True
    else:
        print("remove cancelled")
        return False






