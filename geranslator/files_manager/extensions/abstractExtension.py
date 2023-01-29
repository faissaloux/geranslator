from abc import ABC, abstractmethod

class AbstractExtension(ABC):

    @abstractmethod
    def insert(self, data: dict, file: str):
        pass

    @abstractmethod
    def get_keys(self, file: str) -> list:
        pass
