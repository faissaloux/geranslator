import os
from typing import List

from termspark import TermSpark

from .config.config import Config
from .exceptions.MissingExtension import MissingExtension
from .exceptions.MissingOriginLang import MissingOriginLang
from .exceptions.MissingProvider import MissingProvider
from .exceptions.MissingTargetLang import MissingTargetLang
from .exceptions.OriginLangFileNotFound import OriginLangFileNotFound
from .files_manager.files_manager import FilesManager
from .provider.provider import Provider


class Geranslator:
    provider: str
    lang_dir: str
    lang_files_ext: str
    origin_lang: str
    target_lang: List[str] = []

    def __init__(self):
        self.set_lang_dir(Config().get("lang_dir"))
        self.set_origin_lang(Config().get("origin_lang"))
        self.set_target_lang(Config().get("target_langs"))
        self.set_lang_files_extension(Config().get("lang_files_ext"))
        self.set_provider(Config().get("provider"))

    def translate(self):
        self.make_sure_origin_lang_file_exists()

        text = (
            FilesManager()
            .set_langs_dir(self.lang_dir)
            .set_lang(self.origin_lang)
            .set_extension(self.lang_files_ext)
            .get()
        )

        self.__print_config()

        translation = Provider(self.provider).translate(
            text, self.origin_lang, self.target_lang
        )

        for lang in translation:
            FilesManager().set_langs_dir(self.lang_dir).set_data(
                translation[lang]
            ).set_lang(lang).set_extension(self.lang_files_ext).insert()

    def set_provider(self, provider: str):
        if not len(provider):
            raise MissingProvider()

        self.provider = provider

        return self

    def set_origin_lang(self, lang: str):
        if not len(lang):
            raise MissingOriginLang()

        self.origin_lang = lang

        return self

    def set_target_lang(self, *target_lang: List[str]):
        self.target_lang = []

        if isinstance(target_lang[0], list):
            for lang in target_lang[0]:
                self.target_lang.append(lang)
        elif isinstance(target_lang, tuple):
            for lang in target_lang:
                self.target_lang.append(lang)
        else:
            self.target_lang.append(target_lang[0])

        self.target_lang = list(filter(lambda lang: lang.strip(), self.target_lang))

        if not len(self.target_lang):
            raise MissingTargetLang()

        return self

    def set_lang_dir(self, lang_dir: str):
        self.lang_dir = os.path.join(os.getcwd(), lang_dir)

        return self

    def set_lang_files_extension(self, extension: str):
        if not len(extension):
            raise MissingExtension()

        self.lang_files_ext = extension.lower()

        return self

    def origin_lang_file_exists(self) -> bool:
        self.origin_lang_file = os.path.join(
            self.lang_dir, f"{self.origin_lang}.{self.lang_files_ext}"
        )

        return os.path.exists(self.origin_lang_file)

    def make_sure_origin_lang_file_exists(self):
        if not self.origin_lang_file_exists():
            raise OriginLangFileNotFound(
                os.path.join(self.lang_dir, f"{self.origin_lang}.{self.lang_files_ext}")
            )

    def __print_config(self):
        TermSpark().line().spark()
        TermSpark().spark_left(["CONFIG ", "green"]).set_separator(".").spark()

        languages_dir_line = TermSpark()
        languages_dir_line.spark_left(["languages dir "])
        languages_dir_line.spark_right([f" {self.lang_dir}"])
        languages_dir_line.set_separator(".")
        languages_dir_line.spark()

        extension_line = TermSpark()
        extension_line.spark_left(["extension "])
        extension_line.spark_right([f" {self.lang_files_ext}"])
        extension_line.set_separator(".")
        extension_line.spark()

        provider_line = TermSpark()
        provider_line.spark_left(["provider "])
        provider_line.spark_right([f" {self.provider}"])
        provider_line.set_separator(".")
        provider_line.spark()

        origin_lang_line = TermSpark()
        origin_lang_line.spark_left(["from "])
        origin_lang_line.spark_right([f" {self.origin_lang}"])
        origin_lang_line.set_separator(".")
        origin_lang_line.spark()

        target_langs_line = TermSpark()
        target_langs_line.spark_left(["to "])
        target_langs_line.spark_right([f" {' | '.join(self.target_lang)}"])
        target_langs_line.set_separator(".")
        target_langs_line.spark()

        TermSpark().line().spark()
