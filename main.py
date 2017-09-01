""" Import required libraries """
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']


def give_permissions_to_file(service, file_id, email_list, domain_list):
    permissions = None

    if domain_list and isinstance(list, domain_list):
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

    if email_list and isinstance(list, email_list):
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


def main(title, folder_id, mime_type, domain_list, email_list, service_account_json):
    """ Create a google spreadsheet """

    # We have to write it to a file because
    # gcs library only accepts a file path.
    # Rewrite. Must not use /tmp because it is re-used

    credentials_path = '/tmp/credentials.json'
    with open(credentials_path, "w") as credentials_file:
        credentials_file.write(service_account_json)

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_path, SCOPES)

    service = build('drive', 'v3', credentials=credentials)

    meta_data = {
        'name': title,
        'mimeType': mime_type
    }

    if folder_id:
        meta_data['parents'] = [folder_id]

    req = service.files().create(body=meta_data)
    file = req.execute()

    os.remove(credentials_path)

    response = {}
    response["type"] = "error"

    give_permissions_to_file(
        service=service,
        file_id=file.get("id"),
        domain_list=domain_list,
        email_list=email_list)

    return file
