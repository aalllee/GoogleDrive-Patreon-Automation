import requests
from dotenv import load_dotenv
import os

def configure():
    load_dotenv("secret/.env")



def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def convert_mail(email_str):
    email_str = email_str.lower()
    email_domain = find_between(email_str, "@", ".")

    if email_domain == "googlemail":
        email_str=email_str.replace("googlemail","gmail")

    return email_str



def get_member_details(access_token):
    campaign_id = os.getenv('campaign_id')
    print("CAMP ID", campaign_id)
    url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/members?include=currently_entitled_tiers,address&fields[member]=full_name,email,is_follower,last_charge_date,last_charge_status,lifetime_support_cents,currently_entitled_amount_cents,patron_status&fields[tier]=amount_cents,created_at,description,discord_role_ids,edited_at,patron_count,published,published_at,requires_shipping,title,url&fields[address]=addressee,city,line_1,line_2,phone_number,postal_code,state"
    headers = {"Authorization": f"Bearer {access_token}"}
    all_members = []

    while url:
        response = requests.get(url, headers=headers)#,params=params)#, params=params)


        if response.status_code == 200:
            member_data = response.json().get("data")
            all_members.extend(member_data)

            pagination_info = response.json().get("links", {}).get("next")
            url = pagination_info if pagination_info else None

        else:
            print(f"Request failed with status code {response.status_code}")
            print("Response content:", response.text)
            return None

    return all_members




def get_active_patron_emails():
    configure()
    access_token_env = os.getenv('patreon_access_token')
    members = get_member_details(access_token_env)

    active_patrons = []
    for member in members:
        if member["attributes"]["patron_status"] == "active_patron":
            active_patrons.append(member)

    active_patron_emails = []
    for member in active_patrons:
        member_email = member["attributes"]["email"]
        member_email=convert_mail(member_email)
        active_patron_emails.append(member_email)



    return active_patron_emails



