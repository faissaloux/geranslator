import os

from typing import List
from .config.config import Config
from .provider.provider import Provider
from .files_manager.files_manager import FilesManager
from .exceptions.OriginLangFileNotFound import OriginLangFileNotFound

class Geranslator:
    provider: str
    lang_dir: str
    lang_files_ext: str
    origin_lang: str
    target_lang: List[str] = []

    def __init__(self):
        self.set_lang_dir(Config().get('lang_dir'))
        self.set_origin_lang(Config().get('origin_lang'))
        self.set_target_lang(Config().get('to_langs'))
        self.set_lang_files_extension(Config().get('lang_files_ext'))
        self.set_provider(Config().get('provider'))

    def translate(self):
        self.make_sure_origin_lang_file_exists()

        words = FilesManager().set_dir(self.lang_dir).set_lang(self.origin_lang).set_extension(self.lang_files_ext).get_keys()

        translation = Provider(self.provider).translate(words, self.origin_lang, self.target_lang)

        for lang in translation:
            FilesManager().set_dir(self.lang_dir).set_data(translation[lang]).set_lang(lang).set_extension(self.lang_files_ext).insert()

    def set_provider(self, provider: str):
        self.provider = provider

        return self

    def set_origin_lang(self, lang: str):
        self.origin_lang = lang

        return self

    def set_target_lang(self, *target_lang: List[str]):
        self.target_lang = []

        if (isinstance(target_lang[0], list)):
            for lang in target_lang[0]:
                self.target_lang.append(lang)
        elif isinstance(target_lang, tuple):
            for lang in target_lang:
                self.target_lang.append(lang)
        else:
            self.target_lang.append(target_lang[0])

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
            raise OriginLangFileNotFound(os.path.join(self.lang_dir, f"{self.origin_lang}.{self.lang_files_ext}"))
