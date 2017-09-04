""" Import required libraries """
import os
import json
import tempfile

from google.oauth2 import service_account
from apiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_FILENAME = 'credentials.json'


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

    tmpdir = tempfile.mkdtemp()
    saved_umask = os.umask(0077)

    _cred = None

    path = os.path.join(tmpdir, CREDENTIALS_FILENAME)

    try:
        with open(path, "w") as tmp:
            tmp.write(json.loads(credentials))

        _cred = service_account.Credentials.from_service_account_file(path)
    except IOError:
        print 'IOError'
    else:
        os.remove(path)
    finally:
        os.umask(saved_umask)
        os.rmdir(tmpdir)

    return _cred


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

    give_permissions_to_file(
        service=service,
        file_id=file.get("id"),
        domain_list=domain_list,
        email_list=email_list)

    return file
