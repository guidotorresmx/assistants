import os
import random
import yaml
from collections import Counter
from nltk.corpus import movie_reviews
from nltk.corpus import senseval


class datasetGenerator():
    """
    creates a base dataset from senseval in NLTK

    it generates data.json dataset by instanciating it
    """
    def __init__(self, dataset="", size= 200, filename= "data.json", randomSeed= 42):
        #TODO: if data.json exists, use it
        if dataset == "":
            if "json.data" in os.walk(os.path.join("..","data",filename)):
                return
            else:
                dataset = "senseval"
        if dataset == "senseval":
            self.instances = senseval.instances('hard.pos')
            self.getData()
            self.sampleData(size, randomSeed)
            self.saveData()
        if dataset not in ["","senseval"]:
            raise Exception("not implemented other dataset than senseval")

    def getData(self):
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

    def sampleData(self, size= 200, randomSeed = 42):
        random.seed(randomSeed)
        self.sampleList = random.sample(range(len(self.sentences)),size)
        self.sentences = [self.sentences[i] for i in self.sampleList]
        self.labels    = [self.labels[i]    for i in self.sampleList]
        self.uniqueLabels = dict(Counter(self.labels))

    def saveData(self, filename = "data.yaml"):
        j = {}
        j["sentences"] = self.sentences
        j["labels"] = self.labels
        j["counter"] = self.uniqueLabels
        with open(os.path.join("..","data", filename), 'w') as outfile:
            yaml.dump(j, outfile)

d = datasetGenerator()
