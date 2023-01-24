import os

from typing import List
from .translator.translator import Translator
from .config.config import Config
from .exceptions.OriginLangFileNotFound import OriginLangFileNotFound

class Geranslator:
    lang_dir: str
    lang_files_ext: str
    origin_lang: str
    target_lang: List[str]

    def __init__(self):
        self.set_lang_dir(Config().get('lang_dir'))
        self.set_origin_lang(Config().get('origin_lang'))
        self.set_target_lang(Config().get('to_langs'))
        self.set_lang_files_extension(Config().get('lang_files_ext'))
        self.make_sure_origin_lang_file_exists()

    def translate(self):
        Translator().from_lang(self.origin_lang).to_lang(self.target_lang).translate()

    def set_origin_lang(self, lang: str):
        self.origin_lang = lang

        return self

    def set_target_lang(self, lang: List[str]):
        self.target_lang = lang

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
