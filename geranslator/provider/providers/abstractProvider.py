from abc import ABC, abstractmethod, abstractproperty
from typing import List

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from termspark import TermSpark
from webdriver_manager.chrome import ChromeDriverManager


class AbstractProvider(ABC):
    text_to_translate: dict = {}
    translation: dict

    @abstractproperty
    def url(self) -> str:
        pass

    def __init__(self):
        self.translation = {}

    def translate(self, text: dict, origin_lang: str, target_langs: List[str]) -> dict:
        self.text_to_translate = text

        try:
            self.open_browser()
            self.driver.get(self.url)

            for lang in target_langs:
                if self.choose_languages(origin_lang, lang):
                    self.translation[lang] = {}
                    self.__translate_to(lang)

            self.__join_translations()

            return self.translation
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
        for key, value in self.text_to_translate.items():
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

    @abstractmethod
    def translate_text(self, text: str) -> str:
        pass

    @abstractmethod
    def choose_languages(self, lang_from: str, target_lang: str) -> bool:
        pass

    @abstractmethod
    def search_language(self, language: str) -> bool:
        pass

    def open_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def close_browser(self):
        self.driver.quit()
