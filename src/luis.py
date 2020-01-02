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
from baseAssistant import baseAssistant


class luis(baseAssistant):
    """
    https://github.com/microsoft/Cognitive-LUIS-Python
    https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/blob/9ebf063909771ec6d03cba42ccec9eecdec6e538/samples/language/luis/luis_authoring_samples.py
    """
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


    def getResponse(self, msg = ""):
        raise Exception("not implemented yet!")

    def setData(self, data):
        #change this for group in pandas and yaml for csv
        for key in data.counter.keys:
            for i, label in enumerate(labels):
                if label== key:

        class_name = "Class"
        flight_name = "Flight"

        find_economy_to_madrid = "find flights in economy to Madrid"
        find_first_to_london = "find flights to London in first class"

        intent_name = "FindFlights"
        intent_id = a.assistant.model.add_intent(
            app_id,
            version_id,
            intent_name
        )

        utterance = {
            'text': find_economy_to_madrid,
            'intent_name': intent_name,
            }
        a.assistant.examples.add(
            app_id,
            version_id,
            utterance,
            raw = True
        )


        utterances = [
            {
                'text': find_economy_to_madrid,
                'intent_name': intent_name,
            },
            {
                'text': find_first_to_london,
                'intent_name': intent_name,
            }
        ]


        utterances_result = a.assistant.examples.batch(
            self.app_id,
            self.version_id,
            utterances,
            raw = True
        )


    def update(self):
        async_training = a.assistant.train.train_version(self.app_id, self.version_id, raw = True)

        async_training = a.assistant.train.train_version(self.app_id, self.version_id, raw = False)

        is_trained = async_training.status == "UpToDate"

        trained_status = ["UpToDate", "Success"]
        while not is_trained:
            time.sleep(1)
            status = a.assistant.train.get_status(app_id, version_id)
            is_trained = all(
                m.details.status in trained_status for m in status)

        publish_result = a.assistant.apps.publish(
            app_id,
            version_id = version_id,
            is_staging = False,
            region = 'westus'
        )

        self.endpoint = publish_result.endpoint_url + \
            "?subscription-key=" + a.creds["luis"]["APIKEY"] + "&q="



if __name__() == "__main__":
    a = luis()
    a.update()
    a.getWorkspaceID()
    a.getIntents()
    a.deleteAllIntents()
    async_training = a.assistant.train.train_version(a.app_id, a.version_id, raw = True)
    async_training.response.status
    dir(async_training)
    dir(async_training.response)
