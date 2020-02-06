from abc import ABC, abstractmethod


class baseAssistant(ABC):
    @abstractmethod
    def __init__():
        pass

    @abstractmethod
    def getCreds(self):
        pass

    @abstractmethod
    def getWorkspaceID(self):
        pass

    @abstractmethod
    def getResponse(self):
        pass

    @abstractmethod
    def setData(self):
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

    @abstractmethod
    def update(self):
        pass
