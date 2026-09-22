import os
import json
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Config

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailService:
    def __init__(self):
        self.creds = None

        if Config.GMAIL_TOKEN_JSON:
            try:
                token_data = json.loads(Config.GMAIL_TOKEN_JSON)
                self.creds = Credentials.from_authorized_user_info(token_data, SCOPES)
            except Exception as e:
                print(f"Error parsing GMAIL_TOKEN_JSON: {e}")
        # Fallback to local token.json file
        elif os.path.exists('token.json'):
            try:
                self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            except Exception as e:
                print(f"Error loading token.json: {e}")
        else:
            print("WARNING: No Gmail API token found. Emails will not be sent.")

    def send_email(self, to_email, subject, body):
        if not self.creds:
            print(f"Skipping email to {to_email} (No credentials)")
            return False

        try:
            service = build('gmail', 'v1', credentials=self.creds)
            
            message = EmailMessage()
            message.set_content(body)
            message['To'] = to_email
            message['Subject'] = subject

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {'raw': encoded_message}

            # Send the email
            send_message = (service.users().messages().send(userId="me", body=create_message).execute())
            print(f"Message Id: {send_message['id']}")
            return True
        except HttpError as error:
            print(f"An error occurred sending email: {error}")
            return False

gmail_service = GmailService()
