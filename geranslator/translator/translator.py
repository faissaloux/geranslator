from typing import List

from ..provider.provider import Provider
from ..languages.languages import Languages

class Translator:
    lang_to_files: List[str] = []

    def __init__(self):
        self.lang_to_files = []

    def translate(self):
        Provider().translate(self.lang_from_file, self.lang_to_files)

    def from_lang(self, lang_from_file: str):
        self.lang_from_file = Languages().get(lang_from_file)

        return self
    
    def to_lang(self, *lang_to_files: List[str]):
        if (isinstance(lang_to_files[0], list)):
            for lang in lang_to_files[0]:
                self.lang_to_files.append(Languages().get(lang))
        elif isinstance(lang_to_files, tuple):
            for lang in lang_to_files:
                self.lang_to_files.append(Languages().get(lang))
        else:
            self.lang_to_files.append(Languages().get(lang_to_files[0]))

        return self
