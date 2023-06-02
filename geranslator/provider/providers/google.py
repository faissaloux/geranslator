import time

from selenium.common.exceptions import WebDriverException
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

        try:
            WebDriverWait(self.driver, 15).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//button[@aria-label='Copy translation']")
                )
            )
        except WebDriverException:
            while True:
                try_again = self.driver.find_element(
                    by=By.XPATH,
                    value="//button[contains(@class, 'VfPpkd-LgbsSe')][contains(.,'Try again')]",
                )

                if try_again.is_displayed():
                    try_again.click()
                    time.sleep(6)
                else:
                    break

        translated_element = self.driver.find_element(
            by=By.XPATH, value="//span[@class='HwtZe']"
        )

        translation = translated_element.text.lower()

        self.clear_source_text()

        return translation

    def choose_origin_language(self, origin_lang: str) -> bool:
        TermSpark().spark_left([f"{Languages().get(origin_lang)} "]).spark_right(
            [" CHECKING LANGUAGE", "yellow"]
        ).set_separator(".").spark("\r")

        more_source_languages_btn = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//button[@aria-label='More source languages']")
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
                (By.XPATH, "(//button[@aria-label='More target languages'])[1]")
            )
        )
        time.sleep(1)
        more_target_languages_btn.click()
        target_lang_found = self.search_language(Languages().get(target_lang))

        return target_lang_found

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
                )

                if unexisted_language.is_displayed():
                    TermSpark().spark_left([f"{language} "]).spark_right(
                        [" language not supported by google", "red"]
                    ).set_separator(".").spark()
                    ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    return False
                else:
                    ActionChains(self.driver).send_keys(
                        Keys.DOWN, Keys.RETURN
                    ).perform()
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
                (By.XPATH, "//button[@aria-label='Clear source text']")
            )
        )
        clear_source_text_btn.click()
