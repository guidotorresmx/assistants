import os
import yaml
from abc import ABC, abstractmethod


class baseAssistant(ABC):
    """
        base assistant class
    """
    @abstractmethod
    def __init__():
        pass

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

    @abstractmethod
    def getWorkspaceID(self):
        pass

    @abstractmethod
    def getResponse(self):
        pass

    @abstractmethod
    def getIntents(Self):
        pass

    @abstractmethod
    def deleteIntent(self):
        pass

    @abstractmethod
    def deleteAllIntents(self):
        pass

    @abstractmethod
    def setData(self):
        pass
