import os
import shutil

import pytest

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

    def test_exit_when_origin_lang_is_not_supported(self):
        with pytest.raises(SystemExit):
            Google().translate(
                {"text_1": "good morning", "text_2": "good night"},
                "not_supported",
                ["ar", "fr"],
                Config().get("lang_dir"),
                "json",
            )

    def test_translation_text(self):
        google_provider = Google()
        translation = google_provider.translate(
            {"text_1": "good morning", "text_2": "good night"},
            "en",
            ["ar", "fr"],
            Config().get("lang_dir"),
            "json",
        )

        assert google_provider.text_to_translate == {
            "text_1": "good morning",
            "text_2": "good night",
        }
        assert list(google_provider.translation.keys()) == ["ar", "fr"]
        assert list(google_provider.translation["ar"].keys()) == ["text_1", "text_2"]
        assert list(google_provider.translation["fr"].keys()) == ["text_1", "text_2"]
        assert translation == google_provider.translation
        assert translation == {
            "ar": {"text_1": "صباح الخير", "text_2": "طاب مساؤك"},
            "fr": {"text_1": "bonjour", "text_2": "bonne nuit"},
        }

    def test_translation_returns_lower_case(self):
        google_provider = Google()
        translation = google_provider.translate(
            {"text_1": "GOOD MORNING", "text_2": "GOOD NIGHT"},
            "en",
            ["es", "fr"],
            Config().get("lang_dir"),
            "json",
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
            Config().get("lang_dir"),
            "json",
        )

        assert google_provider.text_to_translate == {
            "text_1": "good morning",
            "text_2": "good night",
        }
        assert list(google_provider.translation.keys()) == ["ar", "fr"]
        assert list(google_provider.translation["ar"].keys()) == ["text_1", "text_2"]
        assert list(google_provider.translation["fr"].keys()) == ["text_1", "text_2"]
        assert translation == google_provider.translation
        assert translation == {
            "ar": {"text_1": "صباح الخير", "text_2": "طاب مساؤك"},
            "fr": {"text_1": "bonjour", "text_2": "bonne nuit"},
        }

    def test_translation_text_includes_hidden_value(self):
        google_provider = Google()
        translation = google_provider.translate(
            {
                "Hello": "hello",
                "morning": {":attribute": ["good morning ", " , see you later!"]},
                "Bye": "bye",
            },
            "en",
            ["ar", "fr"],
            Config().get("lang_dir"),
            "json",
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
        assert translation == google_provider.translation
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

    def test_translation_text_includes_multiple_hidden_values(self):
        google_provider = Google()
        translation = google_provider.translate(
            {
                "morning": {
                    ":attribute1": [
                        "good morning",
                        {":attribute2": [" , see you ", " later!"]},
                    ]
                }
            },
            "en",
            ["ar", "fr"],
            Config().get("lang_dir"),
            "json",
        )

        assert google_provider.text_to_translate == {
            "morning": {
                ":attribute1": [
                    "good morning",
                    {":attribute2": [" , see you ", " later!"]},
                ]
            }
        }
        assert list(google_provider.translation.keys()) == ["ar", "fr"]
        assert list(google_provider.translation["ar"].keys()) == ["morning"]
        assert list(google_provider.translation["fr"].keys()) == ["morning"]
        assert translation == google_provider.translation
        assert translation == {
            "ar": {"morning": "صباح الخير:attribute1، أرك لاحقًا:attribute2لاحقاً!"},
            "fr": {"morning": "bonjour:attribute1, à bientôt:attribute2plus tard!"},
        }
