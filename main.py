from Patreon_requests import get_active_patron_emails
from google_drive_access import get_folder_member_emails
from google_drive_access import remove_members
from dotenv import load_dotenv
import os

active_patron_emails = set(get_active_patron_emails())
print("Active Patron Count: ", len(active_patron_emails))
print(active_patron_emails)

def update_folder_access(active_members, folder_id):
    difference = []
    members_to_add = []
    folder_members = get_folder_member_emails(folder_id)

    for member in folder_members:
        if member not in active_members:
            difference.append(member)

    for member in active_members:
        if member not in folder_members:
            members_to_add.append(member)

    print("MEMBERS THAT ARE ACTIVE BUT HAVE NO ACCESS:", members_to_add)
    print("MEMBERS THAT ARE INACTIVE BUT STILL HAVE ACCESS:", difference)

    remove_members(difference, folder_id)




load_dotenv("secret/.env")
folder_id_cgbreakdown = os.getenv('cg_breakdown_folder_id')
folder_id_tools = os.getenv('tools_folder_id')


update_folder_access(active_patron_emails, folder_id_tools)
update_folder_access(active_patron_emails, folder_id_cgbreakdown)

