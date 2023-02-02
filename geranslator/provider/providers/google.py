import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from termspark import TermSpark
from .abstractProvider import AbstractProvider
from ...languages.languages import Languages

class Google(AbstractProvider):
    url: str = 'https://translate.google.com'

    def translate_for(self, lang: str):
        for key, value in self.text_to_translate.items():
            source_text = WebDriverWait(self.driver, 15).until(
                expected_conditions.presence_of_element_located((
                    By.XPATH, "//textarea[@aria-label='Source text']"
                ))
            )
            ActionChains(self.driver).move_to_element(source_text).click().send_keys(value).perform()

            time.sleep(4)

            WebDriverWait(self.driver, 15).until(
                expected_conditions.presence_of_element_located((
                    By.XPATH, "//button[@aria-label='Copy translation']"
                ))
            )

            translated_element = self.driver.find_element(by=By.XPATH, value="//span[@class='HwtZe']")
            self.translation[lang][key] = translated_element.text
            source_text.clear()

    def choose_languages(self, lang_from: str, target_lang: str) -> bool:
        more_source_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located((
                By.XPATH, "//button[@aria-label='More source languages']"
            ))
        )
        more_source_languages_btn.click()
        origin_lang_found = self.search_language(Languages().get(lang_from))

        more_target_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located((
                By.XPATH, "//button[@aria-label='More target languages']"
            ))
        )
        more_target_languages_btn.click()
        target_lang_found = self.search_language(Languages().get(target_lang))

        return all([origin_lang_found, target_lang_found])

    def search_language(self, language: str) -> bool:
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
                time.sleep(2)
                unexisted_language = self.driver.find_element(by=By.XPATH, value="//div[@class='G3Fn7c'][contains(.,'No results')]").is_displayed()

                if unexisted_language:
                    TermSpark().spark_left([f" {language} ", 'white', 'red'], [f" language not supported ", 'red']).spark()
                    return False
                else:
                    ActionChains(self.driver).send_keys(Keys.DOWN, Keys.RETURN).perform()

                time.sleep(2)
        return True
