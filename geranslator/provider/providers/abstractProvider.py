from abc import ABC, abstractmethod, abstractproperty

from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class AbstractProvider(ABC):

    @abstractproperty
    def url(self) -> str:
        pass

    @abstractmethod
    def translate(self, words: list, origin_lang: str, lang_to_files: List[str]) -> dict:
        pass

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

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()

    def close_browser(self):
        self.driver.quit()
