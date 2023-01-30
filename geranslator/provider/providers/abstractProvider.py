from abc import ABC, abstractmethod, abstractproperty

from typing import List
from selenium import webdriver
from termspark import TermSpark
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

class AbstractProvider(ABC):
    words_to_translate: list = []
    translation: dict

    @abstractproperty
    def url(self) -> str:
        pass

    def __init__(self):
        self.translation = {}

    def translate(self, words: list, origin_lang: str, lang_to_files: List[str]) -> dict:
        try:
            self.open_browser()
            self.driver.get(self.url)

            self.words_to_translate = words

            for lang in lang_to_files:
                self.translation[lang] = {}

                self.choose_languages(origin_lang, lang)

                self.translate_for(lang)

            return self.translation
        except WebDriverException as e:
            TermSpark().spark_left([' Please check your network and try again ', 'white', 'red']).spark()
            return {}

    @abstractmethod
    def translate_for(self, lang: str):
        pass

    @abstractmethod
    def choose_languages(self, lang_from: str, lang_to: str):
        pass

    @abstractmethod
    def search_language(self, language: str):
        pass

    def open_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def close_browser(self):
        self.driver.quit()