import os

from typing import List
from .provider.provider import Provider
from .config.config import Config
from .exceptions.OriginLangFileNotFound import OriginLangFileNotFound

class Geranslator:
    lang_dir: str
    lang_files_ext: str
    origin_lang: str
    target_lang: List[str] = []

    def __init__(self):
        self.set_lang_dir(Config().get('lang_dir'))
        self.set_origin_lang(Config().get('origin_lang'))
        self.set_target_lang(Config().get('to_langs'))
        self.set_lang_files_extension(Config().get('lang_files_ext'))
        self.make_sure_origin_lang_file_exists()

    def translate(self):
        Provider().translate(self.origin_lang, self.target_lang)

    def set_origin_lang(self, lang: str):
        self.origin_lang = lang

        return self

    def set_target_lang(self, *lang: List[str]):
        self.target_lang = []

        if (isinstance(lang[0], list)):
            for lang in lang[0]:
                self.target_lang.append(lang)
        elif isinstance(lang, tuple):
            for lang in lang:
                self.target_lang.append(lang)
        else:
            self.target_lang.append(lang[0])

        return self

    def set_lang_dir(self, lang_dir: str):
        self.lang_dir = os.path.join(os.getcwd(), lang_dir)

        return self

    def set_lang_files_extension(self, extension: str):
        self.lang_files_ext = extension

        return self

    def origin_lang_file_exists(self) -> bool:
        self.origin_lang_file = os.path.join(self.lang_dir, f"{self.origin_lang}.{self.lang_files_ext}")

        return os.path.exists(self.origin_lang_file)

    def make_sure_origin_lang_file_exists(self):
        if not self.origin_lang_file_exists():
            raise OriginLangFileNotFound(f"{self.origin_lang}.{self.lang_files_ext}")
