import os
import time
from abc import ABC, abstractmethod, abstractproperty
from typing import List

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from termspark import TermSpark
from webdriver_manager.chrome import ChromeDriverManager

from ...files_manager.files_manager import FilesManager
from ...languages.languages import Languages


class AbstractProvider(ABC):
    text_to_translate: dict = {}
    translation: dict
    translated_elements_counter: int = 0

    @abstractproperty
    def url(self) -> str:
        pass

    def __init__(self):
        self.translation = {}

    def translate(
        self,
        text: dict,
        origin_lang: str,
        target_langs: List[str],
        langs_dir: str,
        langs_files_ext: str,
        lang_file_prefix: str,
    ) -> dict:
        try:
            TermSpark().spark_left(
                [
                    "wait some seconds ... ",
                ]
            ).spark("\r")
            self.open_browser()
            TermSpark().spark_left(
                [
                    "hold tight ... ",
                ]
            ).spark("\r")
            self.driver.get(self.url)

            if not self.choose_origin_language(origin_lang):
                exit()

            TermSpark().spark_left(["TRANSLATING ", "green"]).set_separator(".").spark()
            for lang in target_langs:
                self.text_to_translate: dict = text.copy()

                self.__skip_translated_keys(
                    lang, langs_dir, langs_files_ext, lang_file_prefix
                )

                if not len(self.text_to_translate):
                    TermSpark().spark_left([f"{Languages().get(lang)} "]).spark_right(
                        [" SKIPPED", "yellow"],
                    ).set_separator(".").spark()

                    continue

                exec_start = time.time()
                if self.choose_target_language(lang):
                    self.translation[lang] = {}
                    self.__translate_to(lang)
                    exec_end = time.time()

                    TermSpark().spark_left([f"{Languages().get(lang)} "]).spark_right(
                        [f" {round(exec_end - exec_start, 2)} sec", "gray"],
                        [" DONE", "green"],
                    ).set_separator(".").spark()

            self.__join_translations()

            self.close_browser()

            return {
                "translation": self.translation,
                "translated_elements_counter": self.translated_elements_counter,
            }
        except WebDriverException:
            TermSpark().spark_left(
                [" Please check your network and try again ", "white", "red"]
            ).spark()

            return {}

    def __join_translations(self):
        for lang, translations in self.translation.items():
            for key, translation in translations.items():
                if isinstance(translation, dict):
                    self.translation[lang][key] = "".join(
                        self.__join_translation_parts(translation)
                    )
                else:
                    self.translation[lang][key] = translation

    def __join_translation_parts(self, translation_parts_dict: dict) -> list:
        joined: list = []

        for hidden, translation_parts in translation_parts_dict.items():
            for index, translation_part in enumerate(translation_parts):
                if isinstance(translation_part, dict):
                    joined.extend(self.__join_translation_parts(translation_part))
                elif not self.__list_has_dict(translation_parts):
                    joined.append(translation_part)
                    if index != len(translation_parts) - 1:
                        joined.append(hidden)
                else:
                    joined.append(translation_part)
                    joined.append(hidden)

        return joined

    def __list_has_dict(self, list: list) -> bool:
        for item in list:
            if isinstance(item, dict):
                return True

        return False

    def __translate_to(self, lang: str):
        counter = 1
        for key, value in self.text_to_translate.items():
            TermSpark().spark_left([f"{Languages().get(lang)} "]).spark_right(
                [f" {counter}/{len(self.text_to_translate)} "],
                [" TRANSLATING", "yellow"],
            ).set_separator(".").spark("\r")
            if isinstance(value, dict):
                for hidden, texts in value.items():
                    for text in texts:
                        if isinstance(text, dict):
                            self.translation[lang][key][hidden].append(
                                self.__translate_dict(text)
                            )
                        else:
                            translation = self.translate_text(text)
                            try:
                                self.translation[lang][key][hidden].append(translation)
                            except KeyError:
                                self.translation[lang][key] = {}
                                self.translation[lang][key][hidden] = []
                                self.translation[lang][key][hidden].append(translation)
            else:
                translation = self.translate_text(value)
                self.translation[lang][key] = translation

            counter += 1
            self.translated_elements_counter += 1

    def __translate_dict(self, text_dict: dict) -> dict:
        result: dict = {}

        for hidden, texts in text_dict.items():
            for text in texts:
                if isinstance(text, dict):
                    result[hidden].append(self.__translate_dict(text))
                else:
                    translation = self.translate_text(text)
                    try:
                        result[hidden].append(translation)
                    except KeyError:
                        result[hidden] = []
                        result[hidden].append(translation)

        return result

    def __skip_translated_keys(
        self, lang: str, langs_dir: str, langs_files_ext: str, lang_file_prefix: str
    ):
        target_lang_file = os.path.join(
            os.getcwd(), langs_dir, f"{lang_file_prefix}{lang}." + langs_files_ext
        )

        if os.path.exists(target_lang_file):
            target_lang_text = (
                FilesManager()
                .set_lang_file(target_lang_file)
                .set_extension(langs_files_ext)
                .get()
            )

            for key in list(self.text_to_translate.keys()):
                if key in target_lang_text.keys():
                    self.text_to_translate.pop(key)

    @abstractmethod
    def translate_text(self, text: str) -> str:
        pass

    @abstractmethod
    def choose_origin_language(self, origin_lang: str) -> bool:
        pass

    @abstractmethod
    def choose_target_language(self, target_lang: str) -> bool:
        pass

    @abstractmethod
    def search_language(self, language: str) -> bool:
        pass

    @abstractmethod
    def clear_source_text(self):
        pass

    def open_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def close_browser(self):
        self.driver.quit()
