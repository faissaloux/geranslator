import json
import re

from .abstractExtension import AbstractExtension


class Json(AbstractExtension):
    hidden: list = ["^:"]

    def insert(self, data: dict, file: str):
        json.dump(data, open(file, "w", encoding="utf-8"), indent=4, ensure_ascii=False)

    def get(self, file: str) -> dict:
        data: dict = {}

        for hidden in self.hidden:
            for key, value in json.load(open(file, "r")).items():
                for word in value.split():
                    if bool(re.search(hidden, word)):
                        data[key] = {}
                        data[key][word] = self.__ignore_hidden(value.split(word))
                        break
                    else:
                        data[key] = value

        return data

    def __ignore_hidden(self, text_list: list) -> list:
        result: list = []

        for hidden in self.hidden:
            for text in text_list:
                for word in text.split():
                    if bool(re.search(hidden, word)):
                        result.append({word: self.__ignore_hidden(text.split(word))})
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
