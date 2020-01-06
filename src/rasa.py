import tensorflow as tf
import logging
tf.get_logger().setLevel(logging.ERROR)

import os
import yaml

from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

import pandas as pd
import json
from baseAssistant import baseAssistant
import requests
import io

class rasa(baseAssistant):
    """
    https://cloud.ibm.com/apidocs/assistant/assistant-icp?code=python#create-intent
    """
    def __init__(self):
        pass

    def getCreds(self, credsPath= None):
        raise Exception("rasa does not use credentials!")

    def getWorkspaceID(self):
        raise Exception("not implemented workspaces in rasa and not needed!")


    def getResponse(self, msg = "bye"):
        def pprint(o):
           print(json.dumps(o, indent=2))

        return interpreter.parse(msg)


    def setData(self, filename = "data.csv"):
        def setIntentData(intent, utterancesList, data):
            data.write(intent + '\n')
            for u in utterancesList:
                data.write(u + '\n')
            return data

        df = pd.read_csv(os.path.join("..","data",filename))

        df["sentences"] = "- " + df["sentences"].astype(str)
        df["labels"] = "## intent:" + df["labels"].astype(str)


        data = io.StringIO()
        filename = os.path.join("..","data","dataRasa.md")
        for label in df["labels"].unique():
            utterancesList = df["sentences"].loc[df["labels"] == label].values
            data = setIntentData(label, utterancesList, data)

        with open(filename, "w+") as file:
            file.write(data.getvalue())

        self.intents = df["labels"].unique()
        self.dataFile = filename


    def getIntents(self):
        return self.intents()

    def deleteIntent(self, intent):
        raise Exception("not implemented yet!")

    def deleteAllIntents(self):
        raise Exception("not implemented yet!")

    def update(self):

        self.training_data = load_data(os.path.join("..","data",self.dataFile))
        self.trainer = Trainer(config.load(os.path.join("..","config","rasaConfig.yaml")))
        self.interpreter = self.trainer.train(self.training_data)
        self.model_directory = self.trainer.persist(os.path.join("..","models","rasaModel"), fixed_model_name="current")


training_data = load_data(os.path.join("..","data","dataRasa2.md"))

trainer = Trainer(config.load(os.path.join("..","config","rasaConfig.yaml")))

# train the model!
interpreter = trainer.train(training_data)

# store it for future use
model_directory = trainer.persist(os.path.join("..","models","rasaModel"), fixed_model_name="current")


# small helper to make dict dumps a bit prettier
def pprint(o):
   print(json.dumps(o, indent=2))


pprint(interpreter.parse("how do i set my printer drivers "))




df = pd.read_csv(os.path.join("..","data","data.csv"))

df["sentences"] = "- " + df["sentences"].astype(str)
df["labels"] = "## intent:" + df["labels"].astype(str)

def setIntentData(intent, utterancesList, data):
    data.write(intent + '\n')
    for u in utterancesList:
        data.write(u + '\n')
    return data

data = io.StringIO()
filename = os.path.join("..","data","dataRasa2.md")
for label in df["labels"].unique():
    utterancesList = df["sentences"].loc[df["labels"] == label].values
    data = setIntentData(label, utterancesList, data)

with open(filename, "w+") as file:
    file.write(data.getvalue())


dir(interpreter)
help(interpreter.default_output_attributes)
interpreter.default_output_attributes()
