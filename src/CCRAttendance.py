from __future__ import print_function
import httplib2
import CCRAttendanceServerInterface
from CCRAttendanceDB import CCRAttendanceDB
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CREDENTIAL_FILE_NAME = 'ccr.attendance.json'

def get_credentials(clientSecret,applicationName,scope):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,CREDENTIAL_FILE_NAME)

    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(clientSecret, scope)
        flow.user_agent = applicationName
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def open_db_interface(clientSecret, applicationName, config_file):
    credentials = get_credentials(clientSecret,applicationName,SCOPES)
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    return CCRAttendanceDB(service,config_file)

def connect_server(endpoint):
    return CCRAttendanceServerInterface(endpoint)
