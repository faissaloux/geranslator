import os
import re

import polib

from .abstractExtension import AbstractExtension


class Po(AbstractExtension):
    hidden: list = ["^%"]

    def insert(self, data: dict, file: str):
        if os.path.exists(file):
            data = self.append_data(data, file)

        with open(file, "w", encoding="utf-8") as f:
            for key, sentence in data.items():
                f.write(f"msgid '{key}'\n")
                f.write(f"msgstr '{sentence}'\n\n")

        self.file_created(file)

    def get(self, file: str) -> dict:
        data: dict = {}
        po = polib.pofile(file)

        for hidden in self.hidden:
            for entry in po:
                for word in entry.msgstr.split():
                    if bool(re.search(hidden, word)):
                        data[entry.msgid] = {}
                        data[entry.msgid][word] = self.ignore_hidden(
                            entry.msgstr.split(word)
                        )
                        break
                    else:
                        data[entry.msgid] = entry.msgstr

        return data
