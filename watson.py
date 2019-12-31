"""
    implements the interface for setting and getting data from watson assistant

    todos:
        create dataset and test it
        create unittests
"""

import os
import yaml
from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

del watson

class watson:
    """
    https://cloud.ibm.com/apidocs/assistant/assistant-icp?code=python#create-intent
    """
    def __init__(self):

        self.creds = self.getCreds()

        self.authenticator = IAMAuthenticator(self.creds["watson"]["APIKEY"])
        self.assistant = AssistantV1(
            version='2018-07-10',
            authenticator=self.authenticator)
        self.assistant.set_service_url(self.creds["watson"]["URL"])

        self.assistant.set_disable_ssl_verification(True)

    def getCreds(self, credsPath= None):
        if credsPath == None:
            credsPath = os.path.join("creds","creds.yaml")
        creds = {}
        with open( credsPath, "r" )  as stream:
            try:
                creds = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return creds

    def getWorkspaceID(self):
        return self.assistant.list_workspaces().get_result()["workspaces"][0]["workspace_id"]


    def getResponse(self, msg = ""):
        response = self.assistant.message(
            workspace_id=self.creds["watson"]["WORKSPACE_ID"],
            input={
                'text': 'bye'
            }
        ).get_result()
        return response

    def setData(self, dataPath = "data.yaml"):

        raise Exception("not implemented yet")

        data = {}
        with open( dataPath , "r" )  as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        for d in data:
            response= self.assistant.create_intent(
                workspace_id=self.creds["watson"]["WORKSPACE_ID"],
                intent=d.intent,
                examples=d.listofUtterances
            ).get_result()

    def getIntents(self):
        #TODO: add pagination
        return self.assistant.list_intents(
                workspace_id=self.creds["watson"]["WORKSPACE_ID"]
                ).get_result()["intents"]

    def deleteIntent(self, intent):
        returnresponse= self.assistant.delete_intent(
            workspace_id=self.creds["watson"]["WORKSPACE_ID"],
            intent=intent["intent"]
        ).get_result()

    def deleteAllIntents(self):
        for intent in self.getIntents()["intents"]:
            self.deleteIntent(intent)

a = watson()
a.getWorkspaceID()
a.getIntents()
