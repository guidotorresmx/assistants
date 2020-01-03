"""
    implements the interface for setting and getting data from LUIS

    todos:
        create dataset and test it
        create unittests
"""
import os
import yaml
import json
import time
import datetime
from pprint import pprint
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials
import pandas as pd
from baseAssistant import baseAssistant
import requests
import urllib

class luis(baseAssistant):
    """
    https://github.com/microsoft/Cognitive-LUIS-Python
    https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/blob/9ebf063909771ec6d03cba42ccec9eecdec6e538/samples/language/luis/luis_authoring_samples.py
    """
    #TODO: update to version 0.3 or 0.2
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

    def getWorkspaceID(self):
        def getApp():
            return self.assistant.apps.list()[0].id
            apps = getApps()
        self.app_id = getApp()
        return self.app_id

    def getIntents(self):
        intents = self.assistant.model.list_intents(self.app_id,self.version_id)
        return [intent.id for intent in intents if intent.name != 'None']

    def deleteIntent(self,intent):
        self.assistant.model.delete_intent(
            self.app_id,
            self.version_id,
            intent,
            delete_utterances = True
            )

    def deleteAllIntents(self):
        for intent in self.getIntents():
            self.deleteIntent(intent)


    def getResponse(self, msg = "bye"):
        response = {}
        try:
            response = requests.get(self.creds["luis"]["ENDPOINT"] + urllib.parse.quote_plus(msg)).json()
        except:
            self.update()
            response = requests.get(self.endpoint + urllib.parse.quote_plus(msg)).json()

        return response["topScoringIntent"]

    def setData(self, filename = "data.csv"):
        def setEntityData(intent, utterancesList):
            intent_id = self.assistant.model.add_intent(
                self.app_id,
                self.version_id,
                intent
            )

            utterances = []
            for utterance in utterancesList:
                utterances.append({'text': utterance, 'intent_name':intent})

            #TODO: simplify
            for i in range(1 + len(utterances)//100):
                utterances_result = self.assistant.examples.batch(
                    self.app_id,
                    self.version_id,
                    utterances[i*100:(i+1)*100]
                )

        df = pd.read_csv(os.path.join("..","data",filename))
        for label in df["labels"].unique():
            utterancesList = df["sentences"].loc[df["labels"] == label].values
            setEntityData(label, utterancesList)

        self.update()

    def update(self):
        #async_training = a.assistant.train.train_version(self.app_id, self.version_id, raw = True)
        async_training = self.assistant.train.train_version(self.app_id, self.version_id, raw = False)
        is_trained = async_training.status == "UpToDate"
        trained_status = ["UpToDate", "Success"]
        while not is_trained:
            time.sleep(1)
            status = self.assistant.train.get_status(self.app_id, self.version_id)
            is_trained = all(
                m.details.status in trained_status for m in status)

        publish_result = self.assistant.apps.publish(
            self.app_id,
            self.version_id,
            is_staging = False,
            region = 'westus'
        )

        self.endpoint = publish_result.endpoint_url + \
            "?subscription-key=" + self.creds["luis"]["APIKEY"] + "&q="
