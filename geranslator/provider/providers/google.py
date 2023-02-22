import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from termspark import TermSpark

from ...languages.languages import Languages
from .abstractProvider import AbstractProvider


class Google(AbstractProvider):
    url: str = "https://translate.google.com"

    def translate_text(self, text: str) -> str:
        source_text = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//textarea[@aria-label='Source text']")
            )
        )

        ActionChains(self.driver).move_to_element(source_text).click().send_keys(
            text
        ).perform()

        time.sleep(4)

        WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//button[@aria-label='Copy translation']")
            )
        )

        translated_element = self.driver.find_element(
            by=By.XPATH, value="//span[@class='HwtZe']"
        )
        translation = translated_element.text.lower()

        source_text.clear()

        return translation

    def choose_languages(self, lang_from: str, target_lang: str) -> bool:
        more_source_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//button[@aria-label='More source languages']")
            )
        )
        more_source_languages_btn.click()
        origin_lang_found = self.search_language(Languages().get(lang_from))

        more_target_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//button[@aria-label='More target languages']")
            )
        )
        more_target_languages_btn.click()
        target_lang_found = self.search_language(Languages().get(target_lang))

        return all([origin_lang_found, target_lang_found])

    def search_language(self, language: str) -> bool:
        WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//input[@aria-label='Search languages']")
            )
        )

        time.sleep(2)

        search_language_elements = self.driver.find_elements(
            by=By.XPATH, value="//input[@aria-label='Search languages']"
        )

        for search_language_element in search_language_elements:
            if search_language_element.size["width"]:
                ActionChains(self.driver).move_to_element(
                    search_language_element
                ).click().send_keys(language).perform()
                time.sleep(2)
                unexisted_language = self.driver.find_element(
                    by=By.XPATH,
                    value="//div[@class='G3Fn7c'][contains(.,'No results')]",
                ).is_displayed()

                if unexisted_language:
                    TermSpark().spark_left([f"{language} "]).spark_right(
                        [" language not supported by google", "red"]
                    ).set_separator(".").spark()
                    return False
                else:
                    ActionChains(self.driver).send_keys(
                        Keys.DOWN, Keys.RETURN
                    ).perform()

                time.sleep(2)
        return True
