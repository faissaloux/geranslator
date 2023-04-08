import os
import re
from abc import ABC, abstractmethod

from termspark import TermSpark


class AbstractExtension(ABC):
    hidden: list = []

    @abstractmethod
    def insert(self, data: dict, file: str):
        pass

    @abstractmethod
    def get(self, file: str) -> dict:
        pass

    def append_data(self, data: dict, file: str) -> dict:
        if os.path.exists(file):
            data.update(self.get(file))

        return data

    def file_created(self, file: str):
        TermSpark().spark_left([f"{file} "]).spark_right(
            [" CREATED", "green"]
        ).set_separator(".").spark()

    def ignore_hidden(self, text_list: list) -> list:
        result: list = []

        for hidden in self.hidden:
            for text in text_list:
                for word in text.split():
                    if bool(re.search(hidden, word)):
                        result.append({word: self.ignore_hidden(text.split(word))})
                        break
                    else:
                        if text not in result and not self.__hidden_in_text(text):
                            result.append(text)
                        continue

        return result

    def __hidden_in_text(self, text: str) -> bool:
        for hidden in self.hidden:
            for word in text.split():
                if bool(re.search(hidden, word)):
                    return True

        return False
