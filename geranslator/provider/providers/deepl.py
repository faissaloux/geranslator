import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from .abstractProvider import AbstractProvider
from ...languages.languages import Languages
from ...exceptions.UnsupportedLanguage import UnsupportedLanguage

class Deepl(AbstractProvider):
    url: str = 'https://www.deepl.com/translator'

    def translate_for(self, lang: str):
        for word_to_translate in self.words_to_translate:
            source_text = WebDriverWait(self.driver, 15).until(
                expected_conditions.presence_of_element_located((
                    By.XPATH, "//textarea[@dl-test='translator-source-input']"
                ))
            )
            ActionChains(self.driver).move_to_element(source_text).click().send_keys(word_to_translate).perform()

            time.sleep(2)

            WebDriverWait(self.driver, 15).until(
                expected_conditions.presence_of_element_located((
                    By.XPATH, "//textarea[@dl-test='translator-target-input']"
                ))
            )

            translated_element = self.driver.find_element(by=By.XPATH, value="//textarea[@dl-test='translator-target-input']")
            self.translation[lang][word_to_translate] = translated_element.get_attribute('value')

            source_text.clear()

    def choose_languages(self, lang_from: str, lang_to: str):
        self.__remove_advertisement()

        more_source_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located((
                By.XPATH, "//button[@dl-test='translator-source-lang-btn']"
            ))
        )
        more_source_languages_btn.click()
        self.search_language(Languages().get(lang_from))

        time.sleep(2)

        more_target_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located((
                By.XPATH, "//button[@dl-test='translator-target-lang-btn']"
            ))
        )
        more_target_languages_btn.click()
        self.search_language(Languages().get(lang_to))

    def search_language(self, language: str):
        WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located((
                By.XPATH, "//input[@placeholder='Search languages']"
            ))
        )

        time.sleep(2)
        search_language_elements = self.driver.find_elements(by=By.XPATH, value="//input[@placeholder='Search languages']")

        for search_language_element in search_language_elements:
            if search_language_element.size['width']:
                ActionChains(self.driver).move_to_element(search_language_element).click().send_keys(language).perform()
                time.sleep(2)
                unexisted_language = self.driver.find_elements(by=By.XPATH, value="//div[@class='lmt__sides_wrapper'][contains(., 'No results')]")

                if len(unexisted_language):
                    raise UnsupportedLanguage(language)
                else:
                    ActionChains(self.driver).send_keys(Keys.RETURN).perform()

                time.sleep(2)

    def __remove_advertisement(self):
        try:
            close_advertisement_popup_btn = WebDriverWait(self.driver, 15).until(
                expected_conditions.presence_of_element_located((
                    By.XPATH, "//div[@data-testid='write-advertisement-popup']/button[@aria-label='Close']"
                ))
            )
            close_advertisement_popup_btn.click()
        except:
            pass
