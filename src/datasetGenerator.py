import os
import random
import yaml
from collections import Counter
from nltk.corpus import movie_reviews
from nltk.corpus import senseval
import pandas as pd
import json



class datasetGenerator():
    """
    creates a base dataset from senseval in NLTK

    it generates data.json dataset by instanciating it

    or by retrieving data from https://github.com/sebischair/NLU-Evaluation-Corpora
    """
    #TODO: consolidate dataflow to pandas dataframe y csv o yaml
    def __init__(self, dataset="", size= 200, filename= "data.json", randomSeed= 42):
        if dataset == "":
            if "json.data" in os.walk(os.path.join("..","data",filename)):
                return
            else:
                dataset = "senseval"
        if dataset == "senseval":
            self.instances = senseval.instances('hard.pos')
            self.getDataNLTK()
            self.sampleData(size, randomSeed)
            self.saveData()
        if dataset == "AskUbuntuCorpus" or dataset == "ChatbotCorpus" or dataset == "WebApplicationsCorpus":
            input()
            self.getDataJson(dataset)
            self.sampleData(size, randomSeed)
            self.saveData()

        if dataset not in ["","senseval","AskUbuntuCorpus","ChatbotCorpus","WebApplicationsCorpus"]:
            raise Exception("not implemented other dataset than senseval")

    def getDataNLTK(self):
        self.labels = []
        self.sentences = []
        for instance in self.instances:
            try:
                self.sentences.append(
                    ' '.join([ i for i, _ in instance.context if i.isalpha()])
                )
                self.labels.append(instance.senses[0])
            except:
                pass

    def getDataJson(self, filename):
        with open(os.path.join("..", "data", filename+".json"),encoding = "utf8") as datafile:
            data = json.load(datafile)

        df = pd.DataFrame(data["sentences"])
        df = df.loc[df["intent"] != 'None']
        self.labels = df.intent.tolist()
        self.sentences = df.text.tolist()

    def sampleData(self, size= 200, randomSeed = 42):
        random.seed(randomSeed)
        self.sampleList = random.sample(range(len(self.sentences)),min(size,len(self.sentences)))
        self.sentences = [self.sentences[i] for i in self.sampleList]
        self.labels    = [self.labels[i]    for i in self.sampleList]
        self.uniqueLabels = dict(Counter(self.labels))

    def saveData(self, filename = "data.csv"):
        df = pd.DataFrame(data = {"sentences": self.sentences, "labels": self.labels})
        df.to_csv(os.path.join("..","data","data.csv"),index= False)

d = datasetGenerator("AskUbuntuCorpus")
