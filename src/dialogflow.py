"""
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/dialogflow/cloud-client
"""

import os
import yaml
import dialogflow_v2
from google.oauth2 import service_account
import uuid
import pandas as pd
from baseAssistant import baseAssistant


class dialogflow(baseAssistant):
    def __init__(self):
        self.project_id = "newagent-jtmdcp"
        self.session_id = str(uuid.uuid4())

        self.creds = self.getCreds()
        self.credentials = service_account.Credentials.from_service_account_info(
            self.creds["dialogflow"]
        )
        self.assistant = dialogflow_v2.SessionsClient(credentials=self.credentials)
        self.intents_client = dialogflow_v2.IntentsClient(credentials=self.credentials)
        self.parent = self.intents_client.project_agent_path(self.project_id)

    def getCreds(self, credsPath=None):
        if credsPath is None:
            credsPath = os.path.join("..", "creds", "creds.yaml")
        creds = {}
        with open(credsPath, "r") as stream:
            try:
                creds = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return creds

    def getWorkspaceID(self):
        return self.assistant.session_path(self.project_id, self.session_id)

    def getResponse(self, msg="bye"):
        text_input = dialogflow_v2.types.TextInput(text=msg, language_code="en-us")
        query_input = dialogflow_v2.types.QueryInput(text=text_input)
        response = self.assistant.detect_intent(
            session=self.assistant, query_input=query_input
        )

        return (response.query_result.intent.display_name,)

    def setData(self, filename="data.csv"):
        def setEntityData(intent, utterancesList):
            text = dialogflow_v2.types.Intent.Message.Text(text="")
            message = dialogflow_v2.types.Intent.Message(text=text)
            intent = dialogflow_v2.types.Intent(
                display_name=intent, training_phrases=utterancesList, messages=[message]
            )
            self.intents_client.create_intent(self.parent, intent)

        df = pd.read_csv(os.path.join("..", "data", filename))
        for label in df["labels"].unique():
            utterancesList = df["sentences"].loc[df["labels"] == label].values

            training_phrases = []
            for utterance in utterancesList:
                part = dialogflow_v2.types.Intent.TrainingPhrase.Part(text=utterance)
                training_phrase = dialogflow_v2.types.Intent.TrainingPhrase(
                    parts=[part]
                )
                training_phrases.append(training_phrase)

            setEntityData(label, utterancesList=training_phrases)

    def getIntents(self, name=False):
        """
        The strucutre of intents is as follows:

            [name: "projects/project_name/agent/intents/xxxxx-xxxxxxxx-xxxxxx"
             display_name: "readable intent name"
             priority: priority_number
             messages {
               text {
               }
             },

        the non readable form is needed for deletion
        """
        intents = self.intents_client.list_intents(self.parent)
        if name is True:
            return [intent.name.split("/")[-1] for intent in intents]
        return [intent.display_name for intent in intents]

    def deleteIntent(self, intent):
        intent_path = self.intents_client.intent_path(self.project_id, intent)
        self.intents_client.delete_intent(intent_path)

    def deleteAllIntents(self):
        intents = self.getIntents(name=True)
        for intent in intents:
            self.deleteIntent(intent)

    def update(self):
        pass


if __name__ == "__main__":
    a = dialogflow()
    a.getIntents()
    a.deleteAllIntents()
    a.getIntents()
    a.setData()
    a.getIntents()
