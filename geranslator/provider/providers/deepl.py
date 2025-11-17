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
                (By.XPATH, "//*[@data-testid='translator-source-input']")
            )
        )
        ActionChains(self.driver).move_to_element(source_text).click().send_keys(
            text
        ).perform()

        WebDriverWait(self.driver, 40).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//*[@data-testid='translator-target-input']")
            )
        )

        time.sleep(4)

        translated_element = self.driver.find_element(
            By.XPATH, "//*[@data-testid='translator-target-input']"
        )

        translation = translated_element.get_attribute("value").lower()
        translation = self.__removePunctuationMarkIfNotDemanded(text, translation)

        # Add missing spaces at the end of translation.
        if (space := len(text) - len(text.rstrip())) > 0 and len(translation) == len(
            translation.rstrip()
        ):
            translation = translation + " " * space

        self.clear_source_text()

        return translation

    def choose_origin_language(self, origin_lang: str) -> bool:
        # Wait for the page to load,
        # so we can interact with language search.
        WebDriverWait(self.driver, 120).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, "//div[@data-layout-id='configurationBarLanguagesRow']")
            )
        )
        time.sleep(4)

        TermSpark().spark_left([f"{Languages().get(origin_lang)} "]).spark_right(
            [" CHECKING LANGUAGE", "yellow"]
        ).set_separator(".").spark("\r")

        more_source_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//button[@data-testid='translator-source-lang-btn']")
            )
        )
        more_source_languages_btn.click()
        origin_lang_found = self.search_language(Languages().get(origin_lang))

        return origin_lang_found

    def choose_target_language(self, target_lang: str) -> bool:
        TermSpark().spark_left([f"{Languages().get(target_lang)} "]).spark_right(
            [" CHECKING LANGUAGE", "yellow"]
        ).set_separator(".").spark("\r")

        more_target_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//button[@data-testid='translator-target-lang-btn']")
            )
        )
        more_target_languages_btn.click()
        target_lang_found = self.search_language(Languages().get(target_lang))

        return target_lang_found

    def search_language(self, language: str) -> bool:
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[starts-with(@data-testid, 'translator-lang-option')]",
                )
            )
        )

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
                    value="//div[@data-radix-popper-content-wrapper=''][contains(., 'No results')]",
                )

                if len(unexisted_language):
                    TermSpark().spark_left([f"{language} "]).spark_right(
                        [" language not supported by deepl", "red"]
                    ).set_separator(".").spark()

                    ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    return False
                else:
                    ActionChains(self.driver).send_keys(Keys.RETURN).perform()
                    TermSpark().spark_left(
                        [f"{Languages().get(language)} "]
                    ).spark_right([" LANGUAGE IS SUPPORTED", "blue"]).set_separator(
                        "."
                    ).spark(
                        "\r"
                    )

                time.sleep(2)
        return True

    def clear_source_text(self):
        clear_source_text_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//button[@data-testid='translator-source-clear-button']")
            )
        )
        clear_source_text_btn.click()
        time.sleep(2)

    def __removePunctuationMarkIfNotDemanded(
        self, source: str, translation: str
    ) -> str:
        stripped_translation: str = translation.rstrip()
        if (punctuation := stripped_translation[-1]) in [".", "?", "!"]:
            if source[-1] != punctuation:
                translation = stripped_translation[:-1]

        return translation
