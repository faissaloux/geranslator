import time

from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from ...languages.languages import Languages
from ...files_manager.files_manager import FilesManager
from ...exceptions.UnsupportedLanguage import UnsupportedLanguage

class Google:
    url: str = 'https://translate.google.com'
    to_translate: list = []
    translated: dict

    def __init__(self):
        self.translated = {}

    def translate(self, lang_from_file: str, lang_to_files: List[str]):
        self.open_browser()
        self.driver.get(self.url)

        self.__get_words_to_translate(lang_from_file)

        for lang in lang_to_files:
            self.translated[lang] = {}

            self.__choose_languages(lang_from_file, lang)

            self.__translate_for(lang)

            FilesManager().set_data(self.translated[lang]).set_lang(lang).insert()

    def __translate_for(self, lang):
        for word_to_translate in self.to_translate:
            source_text = WebDriverWait(self.driver, 15).until(
                expected_conditions.presence_of_element_located((
                    By.XPATH, "//textarea[@aria-label='Source text']"
                ))
            )
            ActionChains(self.driver).move_to_element(source_text).click().send_keys(word_to_translate).perform()

            time.sleep(2)

            WebDriverWait(self.driver, 15).until(
                expected_conditions.presence_of_element_located((
                    By.XPATH, "//button[@aria-label='Copy translation']"
                ))
            )

            translated_element = self.driver.find_element(by=By.XPATH, value="//span[@class='HwtZe']")
            self.translated[lang][word_to_translate] = translated_element.text
            source_text.clear()

    def __get_words_to_translate(self, lang):
        self.to_translate = FilesManager().set_lang(lang).get_keys()

    def __choose_languages(self, lang_from, lang_to):
        more_source_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located((
                By.XPATH, "//button[@aria-label='More source languages']"
            ))
        )
        more_source_languages_btn.click()
        self.__search_language(Languages().get(lang_from))

        time.sleep(2)

        more_target_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located((
                By.XPATH, "//button[@aria-label='More target languages']"
            ))
        )
        more_target_languages_btn.click()
        self.__search_language(Languages().get(lang_to))

    def __search_language(self, language):
        WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located((
                By.XPATH, "//input[@aria-label='Search languages']"
            ))
        )

        time.sleep(2)

        search_language_elements = self.driver.find_elements(by=By.XPATH, value="//input[@aria-label='Search languages']")

        for search_language_element in search_language_elements:
            if search_language_element.size['width']:
                ActionChains(self.driver).move_to_element(search_language_element).click().send_keys(language).perform()
                unexisted_language = self.driver.find_element(by=By.XPATH, value=f"//div[@class='G3Fn7c'][contains(.,'No results')]").is_displayed()

                if unexisted_language:
                    raise UnsupportedLanguage(language)
                else:
                    ActionChains(self.driver).send_keys(Keys.DOWN, Keys.RETURN).perform()

                time.sleep(2)

    def open_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()

    def close_browser(self):
        self.driver.quit()
