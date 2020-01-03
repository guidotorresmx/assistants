import os
import yaml
import json
import dialogflow_v2
from google.oauth2 import service_account


dialogflow_key = json.load(open(os.path.join("..","creds","dialogflowCred.json")))

credentials = (service_account.Credentials.from_service_account_info(dialogflow_key))

session_client = dialogflow_v2.SessionsClient(credentials=credentials)

client = dialogflow_v2.AgentsClient(credentials=session_client)

dir(client)

#https://dialogflow-python-client-v2.readthedocs.io/en/latest/


def __init__(self):
    #TODO: try with yaml app id, else: fall down to get onlien workspaces
    self.creds = self.getCreds()
    self.assistant = LUISAuthoringClient(
        'https://westus.api.cognitive.microsoft.com',
        CognitiveServicesCredentials(self.creds["luis"]["APIKEY"]),
    )
    self.app_id = self.getWorkspaceID()
    self.version_id = "0.1"

def getCreds(self, credsPath = None):
    if credsPath == None:
        credsPath = os.path.join("..","creds","creds.yaml")
    creds = {}
    with open( credsPath, "r" )  as stream:
        try:
            creds = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return creds
