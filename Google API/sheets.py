from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.discovery import build
import httplib2
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
import webbrowser

'''
Script load credentials for later requests for google sheet API
'''

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def acquire_new_oauth2_credentials_analytics(secrets_file):
    flow = flow_from_clientsecrets(
        secrets_file,
        scope=SCOPES,
        redirect_uri="http://localhost")
    auth_uri = flow.step1_get_authorize_url()
    webbrowser.open(auth_uri)
    print("Please enter the following URL in a browser " + auth_uri)
    auth_code = input("Enter the authentication code: ")
    credentials = flow.step2_exchange(auth_code)
    return credentials

secrets_file = 'credentials_ga.json'
WEBMASTER_CREDENTIALS_FILE_PATH = "webmaster_credentials.dat"
storage = Storage(WEBMASTER_CREDENTIALS_FILE_PATH)
credentials = acquire_new_oauth2_credentials_analytics(secrets_file)
storage.put(credentials)

http = httplib2.Http()
http = credentials.authorize(http)

def sheet_service():
    sheet = build('sheets', 'v4', credentials=credentials)
    return sheet