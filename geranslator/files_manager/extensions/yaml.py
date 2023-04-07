import re

import yaml

from .abstractExtension import AbstractExtension


class Yaml(AbstractExtension):
    hidden: list = ["^%.+%$"]

    def insert(self, data: dict, file: str):
        yaml.dump(
            self.append_data(data, file),
            open(file, "w", encoding="utf-8"),
            allow_unicode=True,
        )

        self.file_created(file)

    def get(self, file: str) -> dict:
        data: dict = {}

        for hidden in self.hidden:
            for key, value in yaml.load(
                open(file, "r", encoding="utf-8"), Loader=yaml.Loader
            ).items():
                for word in value.split():
                    if bool(re.search(hidden, word)):
                        data[key] = {}
                        data[key][word] = self.ignore_hidden(value.split(word))
                        break
                    else:
                        data[key] = value

        return data
