from abc import ABC, abstractmethod


class DataToPrepare(ABC):
    @abstractmethod
    def format(self):
        pass

    @abstractmethod
    def normalize(self):
        pass

    @abstractmethod
    def interpolate(self):
        pass
