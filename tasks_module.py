import gflags
import httplib2
import logging
import pprint
import sys
import unicodedata

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications <http://code.google.com/apis/accounts/docs/OAuth2.html#IA>
# The client_id client_secret are copied from the API Access tab on
# the Google APIs Console <http://code.google.com/apis/console>. When
# creating credentials for this application be sure to choose an Application
# type of "Installed application".
FLOW = OAuth2WebServerFlow(
    client_id='365336242580.apps.googleusercontent.com',
    client_secret='zB6NBVt0CKHphmzSmmqd-axi',
    scope='https://www.googleapis.com/auth/tasks.readonly',
    user_agent='moderator-cmdline-sample/1.0')

class TasksModule():
  def __init__(self, printer):
    self.printer = printer

  def run(self):
    # If the Credentials don't exist or are invalid run through the native
    # client flow. The Storage object will ensure that if successful the good
    # Credentials will get written back to a file.
    storage = Storage('tasks.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
      credentials = run(FLOW, storage)

    # Create an httplib2.Http object to handle our HTTP requests and authorize
    # it with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build("tasks", "v1", http=http)

    try:
      id = service.tasklists().list().execute()['items'][0]['id']

      response = service.tasks().list(tasklist=id).execute()

      self.printer.PrintHeading("Tasks")
      for item in response['items']:
        #print item['title']
        title = unicodedata.normalize('NFKD', item['title']).encode('ascii',
                                                                    'ignore')
        self.printer.Print(title)
        self.printer.Print(" ")

    except AccessTokenRefreshError:
      print ("The credentials have been revoked or expired, please re-run"
        "the application to re-authorize")

if __name__ == '__main__':
  module = TasksModule()
  module.run()
