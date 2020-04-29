from apiclient.discovery import build
import httplib2
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
import webbrowser

"""
Scripts load credentials from secrets_file and build request body for later request.
"""


def acquire_new_oauth2_credentials_analytics(secrets_file):
    flow = flow_from_clientsecrets(
        secrets_file,
        scope="https://www.googleapis.com/auth/analytics.readonly",
        redirect_uri="http://localhost")
    auth_uri = flow.step1_get_authorize_url()
    webbrowser.open(auth_uri)
    print("Please enter the following URL in a browser " + auth_uri)
    auth_code = input("Enter the authentication code: ")
    credentials = flow.step2_exchange(auth_code)
    return credentials

ANALYTICS_SCOPE = ['https://www.googleapis.com/auth/analytics.readonly']
SPREADSHEET_SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

secrets_file = 'credentials_ga.json'

view_id = {'VIEW_NAME': 'VIEW_ID', 'VIEW_NAME': 'VIEW_ID', 'VIEW_NAME': 'VIEW_ID', 'VIEW_NAME': 'VIEW_ID'}

WEBMASTER_CREDENTIALS_FILE_PATH = "webmaster_credentials.dat"
# Check https://developers.google.com/webmaster-tools/search-console-api-original/v3/ for all available scopes

REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

storage = Storage(WEBMASTER_CREDENTIALS_FILE_PATH)
storage.put(credentials)

http = httplib2.Http()
http = credentials.authorize(http)

# Build the service object.
def analytics_service():
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics


def ga_request(metrics, dimensions, serwis, start_date, end_date, *args):
  return {
        'reportRequests': [
        {
          'viewId': view_id[serwis],
          'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
          'metrics': [{'expression': 'ga:'+metric} for metric in metrics],
          'dimensions': [{'name': 'ga:'+dimension} for dimension in dimensions]
        }]
      }