import os
import polib
import shutil

class Po:

    def insert(self, data: dict, file):
        lang_directory = os.path.dirname(os.path.realpath(file))
        lang_file_sample = os.path.join(lang_directory, os.listdir(lang_directory)[0])

        shutil.copy(lang_file_sample, file)

        po = polib.pofile(file)

        for entry in po:
            entry.msgstr = data[entry.msgid]

        po.save()

    def get_keys(self, file) -> list:
        keys: list = []
        po = polib.pofile(file)

        for entry in po:
            keys.append(entry.msgid)

        return keys
