import re

import yaml

from .abstractExtension import AbstractExtension


class Yaml(AbstractExtension):
    hidden: list = ["^%.+%$"]

    def insert(self, data: dict, file: str):
        yaml.dump(data, open(file, "w"), allow_unicode=True)

    def get(self, file: str) -> dict:
        data: dict = {}

        for hidden in self.hidden:
            for key, value in yaml.load(open(file, "r"), Loader=yaml.Loader).items():
                for word in value.split():
                    if bool(re.search(hidden, word)):
                        data[key] = {}
                        data[key][word] = value.split(word)
                        break
                    else:
                        data[key] = value

        return data
