from abc import ABC, abstractmethod


class AbstractExtension(ABC):
    hidden: list = []

    @abstractmethod
    def insert(self, data: dict, file: str):
        pass

    @abstractmethod
    def get(self, file: str) -> dict:
        pass
