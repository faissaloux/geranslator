import json
import re

from .abstractExtension import AbstractExtension


class Json(AbstractExtension):
    hidden: list = ["^:"]

    def insert(self, data: dict, file: str):
        json.dump(
            self.append_data(data, file),
            open(file, "w", encoding="utf-8"),
            indent=4,
            ensure_ascii=False,
        )

        self.file_created(file)

    def get(self, file: str) -> dict:
        data: dict = {}

        for hidden in self.hidden:
            for key, value in json.load(open(file, "r", encoding="utf-8")).items():
                for word in value.split():
                    if bool(re.search(hidden, word)):
                        data[key] = {}
                        data[key][word] = self.ignore_hidden(value.split(word))
                        break
                    else:
                        data[key] = value

        return data
