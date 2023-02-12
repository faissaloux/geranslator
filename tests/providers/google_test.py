import os
import shutil
from unittest.mock import MagicMock, patch

import pytest
from selenium.common.exceptions import WebDriverException

from geranslator.config.config import Config
from geranslator.provider.providers.google import Google


@pytest.fixture(autouse=True)
def before_and_after_test():
    lang_dir = Config().get("lang_dir")

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.json", "w")
    lang_file.write('{"text_1": "good morning", "text_2": "good night"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)


class TestGoogleProvider:
    def test_url(self):
        assert Google().url == "https://translate.google.com"

    @patch.object(Google, "translate", MagicMock(side_effect=WebDriverException()))
    def test_exception(self):
        with pytest.raises(WebDriverException):
            translation = Google().translate(
                {"text_1": "good morning", "text_2": "good night"}, "en", ["ar", "fr"]
            )

            assert translation == {}

    def test_translation_text(self):
        google_provider = Google()
        translation = google_provider.translate(
            {"text_1": "good morning", "text_2": "good night"}, "en", ["ar", "fr"]
        )

        assert google_provider.text_to_translate == {
            "text_1": "good morning",
            "text_2": "good night",
        }
        assert list(google_provider.translation.keys()) == ["ar", "fr"]
        assert list(google_provider.translation["ar"].keys()) == ["text_1", "text_2"]
        assert list(google_provider.translation["fr"].keys()) == ["text_1", "text_2"]
        assert google_provider.translation["ar"] == {
            "text_1": "صباح الخير",
            "text_2": "طاب مساؤك",
        }
        assert google_provider.translation["fr"] == {
            "text_1": "bonjour",
            "text_2": "bonne nuit",
        }
        assert translation == {
            "ar": {"text_1": "صباح الخير", "text_2": "طاب مساؤك"},
            "fr": {"text_1": "bonjour", "text_2": "bonne nuit"},
        }

    def test_translation_returns_lower_case(self):
        google_provider = Google()
        translation = google_provider.translate(
            {"text_1": "GOOD MORNING", "text_2": "GOOD NIGHT"}, "en", ["es", "fr"]
        )

        assert translation == {
            "es": {"text_1": "buen día", "text_2": "buenas noches"},
            "fr": {"text_1": "bonjour", "text_2": "bonne nuit"},
        }

    def test_language_not_found_doesnt_stop_the_process(self):
        google_provider = Google()
        translation = google_provider.translate(
            {"text_1": "good morning", "text_2": "good night"},
            "en",
            ["ar", "not_exist", "fr"],
        )

        assert google_provider.text_to_translate == {
            "text_1": "good morning",
            "text_2": "good night",
        }
        assert list(google_provider.translation.keys()) == ["ar", "fr"]
        assert list(google_provider.translation["ar"].keys()) == ["text_1", "text_2"]
        assert list(google_provider.translation["fr"].keys()) == ["text_1", "text_2"]
        assert google_provider.translation["ar"] == {
            "text_1": "صباح الخير",
            "text_2": "طاب مساؤك",
        }
        assert google_provider.translation["fr"] == {
            "text_1": "bonjour",
            "text_2": "bonne nuit",
        }
        assert translation == {
            "ar": {"text_1": "صباح الخير", "text_2": "طاب مساؤك"},
            "fr": {"text_1": "bonjour", "text_2": "bonne nuit"},
        }

    def test_translation_text_incldes_hidden_values(self):
        google_provider = Google()
        translation = google_provider.translate(
            {
                "Hello": "hello",
                "morning": {":attribute": ["good morning ", " , see you later!"]},
                "Bye": "bye",
            },
            "en",
            ["ar", "fr"],
        )

        assert google_provider.text_to_translate == {
            "Hello": "hello",
            "morning": {":attribute": ["good morning ", " , see you later!"]},
            "Bye": "bye",
        }
        assert list(google_provider.translation.keys()) == ["ar", "fr"]
        assert list(google_provider.translation["ar"].keys()) == [
            "Hello",
            "morning",
            "Bye",
        ]
        assert list(google_provider.translation["fr"].keys()) == [
            "Hello",
            "morning",
            "Bye",
        ]

        assert google_provider.translation["ar"] == {
            "Hello": "مرحبًا",
            "morning": "صباح الخير:attribute، أراك لاحقًا!",
            "Bye": "الوداع",
        }
        assert google_provider.translation["fr"] == {
            "Hello": "bonjour",
            "morning": "bonjour:attribute, à plus tard!",
            "Bye": "au revoir",
        }
        assert translation == {
            "ar": {
                "Hello": "مرحبًا",
                "morning": "صباح الخير:attribute، أراك لاحقًا!",
                "Bye": "الوداع",
            },
            "fr": {
                "Hello": "bonjour",
                "morning": "bonjour:attribute, à plus tard!",
                "Bye": "au revoir",
            },
        }
