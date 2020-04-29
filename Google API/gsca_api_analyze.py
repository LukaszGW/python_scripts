import httplib2
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
import webbrowser
from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from statistics import mean
import time

"""
Script load credentials and build body request for later requests
"""

def acquire_new_oauth2_credentials(secrets_file):
    flow = flow_from_clientsecrets(
        secrets_file,
        scope="https://www.googleapis.com/auth/webmasters.readonly",
        redirect_uri="http://localhost")
    auth_uri = flow.step1_get_authorize_url()
    webbrowser.open(auth_uri)
    print("Please enter the following URL in a browser " + auth_uri)
    auth_code = input("Enter the authentication code: ")
    credentials = flow.step2_exchange(auth_code)
    return credentials

WEBMASTER_CREDENTIALS_FILE_PATH = "webmaster_credentials.dat"
secrets_file = 'C:\\python\\credentials.json'
# Check https://developers.google.com/webmaster-tools/search-console-api-original/v3/ for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

storage = Storage(WEBMASTER_CREDENTIALS_FILE_PATH)
credentials = acquire_new_oauth2_credentials(secrets_file)
storage.put(credentials)

http = httplib2.Http()
http = credentials.authorize(http)

webmasters_service = build('webmasters', 'v3', http=http)

property_uri = 'Enter_Property_From_GSC'
def build_request(filters, start_date, end_date, dimensions, row, row_limit, aggregationType):
    if filters:
      request_api = {
          'startDate': start_date,
          'endDate': end_date,
          'dimensions': dimensions,
          'dimensionFilterGroups':
              [{
                  'groupType': 'and',
                  'filters': filters}],
          "rowLimit": row_limit,
          "searchType": 'web',
          "aggregationType": aggregationType
      }
      return request_api
    else:
      request_api = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions,
        "startRow": row,
        "rowLimit": row_limit,
        "aggregationType": aggregationType
      }
      return request_api

