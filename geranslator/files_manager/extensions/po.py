import os
import re
import shutil

import polib

from .abstractExtension import AbstractExtension


class Po(AbstractExtension):
    hidden: list = ["^%"]

    def insert(self, data: dict, file: str):
        lang_directory = os.path.dirname(os.path.realpath(file))
        lang_file_sample = os.path.join(lang_directory, os.listdir(lang_directory)[0])

        shutil.copy(lang_file_sample, file)

        po = polib.pofile(file)

        for entry in po:
            entry.msgstr = data[entry.msgid]

        po.save()

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
