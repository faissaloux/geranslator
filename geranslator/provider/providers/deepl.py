import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from termspark import TermSpark

from ...languages.languages import Languages
from .abstractProvider import AbstractProvider


class Deepl(AbstractProvider):
    url: str = "https://www.deepl.com/translator"

    def translate_text(self, text: str) -> str:
        source_text = WebDriverWait(self.driver, 40).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//*[@dl-test='translator-source-input']")
            )
        )
        ActionChains(self.driver).move_to_element(source_text).click().send_keys(
            text
        ).perform()

        time.sleep(4)

        WebDriverWait(self.driver, 40).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//*[@dl-test='translator-target-input']")
            )
        )

        time.sleep(4)

        translated_element = self.driver.find_element(
            By.XPATH, "//*[@dl-test='translator-target-input']"
        )
        time.sleep(1)

        if self.driver.find_elements(
            By.XPATH, "//*[@dl-test='translator-source-input']//p"
        ):
            self.driver.find_element(
                By.XPATH, "//*[@dl-test='translator-source-input']//p"
            ).clear()

        time.sleep(2)

        return translated_element.get_attribute("value").lower()

    def choose_languages(self, lang_from: str, target_lang: str) -> bool:
        self.__remove_advertisement()

        more_source_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//button[@dl-test='translator-source-lang-btn']")
            )
        )
        more_source_languages_btn.click()
        origin_lang_found = self.search_language(Languages().get(lang_from))

        more_target_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//button[@dl-test='translator-target-lang-btn']")
            )
        )
        more_target_languages_btn.click()
        target_lang_found = self.search_language(Languages().get(target_lang))

        return all([origin_lang_found, target_lang_found])

    def search_language(self, language: str) -> bool:
        WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Search languages']")
            )
        )

        time.sleep(2)
        search_language_elements = self.driver.find_elements(
            by=By.XPATH, value="//input[@placeholder='Search languages']"
        )

        for search_language_element in search_language_elements:
            if search_language_element.size["width"]:
                ActionChains(self.driver).move_to_element(
                    search_language_element
                ).click().send_keys(language).perform()
                time.sleep(2)
                unexisted_language = self.driver.find_elements(
                    by=By.XPATH,
                    value="//div[@class='lmt__sides_wrapper'][contains(., 'No results')]",
                )

                if len(unexisted_language):
                    TermSpark().spark_left(
                        [f" {language} ", "white", "red"],
                        [f" language not supported ", "red"],
                    ).spark()
                    return False
                else:
                    ActionChains(self.driver).send_keys(Keys.RETURN).perform()

                time.sleep(2)
        return True

    def __remove_advertisement(self):
        try:
            close_advertisement_popup_btn = WebDriverWait(self.driver, 15).until(
                expected_conditions.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[@data-testid='write-advertisement-popup']/button[@aria-label='Close']",
                    )
                )
            )
            close_advertisement_popup_btn.click()
        except:
            pass
