""" Import required libraries """
import os
import json
from google.oauth2 import service_account
from apiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH = './tmp/credentials.json'


def give_permissions_to_file(service, file_id, email_list, domain_list):
    """
        Give permission to list of domain, or to list of email
    """
    permissions = None

    if domain_list and isinstance(domain_list, list):
        permissions = {
            'type': 'domain',
            'role': 'writer',
            'allowFileDiscovery': True
        }

        for domain in domain_list:
            permissions['domain'] = domain

            req = service.permissions().create(
                fileId=file_id,
                body=permissions,
                fields="id"
            )

            req.execute()

    if email_list and isinstance(email_list, list):
        permissions = {
            'type': 'user',
            'role': 'writer',
        }

        for email in email_list:
            permissions['emailAddress'] = email

            req = service.permissions().create(
                fileId=file_id,
                body=permissions,
                fields="id"
            )

            req.execute()


def get_credentials(credentials):
    """
        We have to write it to a file because gcs
        library only accepts a file path.
    """

    with open(CREDENTIALS_PATH, "w") as credentials_file:
        credentials_file.write(json.loads(credentials))

    return service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH)


def main(title, folder_id, mime_type, service_account_json, domain_list=[], email_list=[]):
    """ Create a google spreadsheet """

    credentials = get_credentials(service_account_json)

    if email_list:
        email_list = json.loads(email_list)

    if domain_list:
        domain_list = json.loads(domain_list)

    service = build('drive', 'v3', credentials=credentials)

    meta_data = {
        'name': title,
        'mimeType': mime_type
    }

    if folder_id:
        meta_data['parents'] = [folder_id]

    req = service.files().create(body=meta_data)
    file = req.execute()

    os.remove(CREDENTIALS_PATH)

    give_permissions_to_file(
        service=service,
        file_id=file.get("id"),
        domain_list=domain_list,
        email_list=email_list)

    return file
