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
                        data[key][word] = value.split(word)
                        break
                    else:
                        data[key] = value

        return data
