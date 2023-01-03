from __future__ import print_function

import os.path
import base64
import sys
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def main():
    # creds = validate_creds()
    collect_names()
    #gmail_create_send(to_addr='dylan.oldfield@yahoo.com', from_addr='Santa', subject='Your Secret Santa', msg='Ho Ho Ho')
    

def collect_names():
    print("Please type the emails of those invited to play the game. Once done type: Done and hit enter")
    current_name = None
    names = []
    for line in sys.stdin:
        if 'done' == line.rstrip().lower():
            break
        elif 'y' == line.rstrip().lower() and current_name:
            print(f'Added {current_name}\n')
            names.append(current_name)
            current_name = None
        elif 'n' == line.rstrip().lower() and current_name:
            print('Ok...please add it again\n')
        else:
            print(f'You added: {line.rstrip().lower()} is this correct? [Y|N] \n')
            current_name = line.rstrip().lower()

    print("Done")


def validate_creds():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def gmail_create_send(to_addr, from_addr, subject, msg):
    """Create and send an email message
        Print the returned  message id
        Returns: Message object, including message id
    
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content('Your Secret Santa is: ')

        message['To'] = to_addr
        message['From'] = from_addr
        message['Subject'] = subject

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


if __name__ == '__main__':
    main()