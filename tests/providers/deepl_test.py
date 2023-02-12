import os
import shutil

import pytest

from geranslator.config.config import Config
from geranslator.provider.providers.deepl import Deepl


@pytest.fixture(autouse=True)
def before_and_after_test():
    lang_dir = Config().get("lang_dir")

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.json", "w")
    lang_file.write('{"text_1": "hello", "text_2": "bye"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)


class TestDeeplProvider:
    def test_url(self):
        assert Deepl().url == "https://www.deepl.com/translator"

    def test_translation_text(self):
        deepl_provider = Deepl()
        translation = deepl_provider.translate(
            {"text_1": "hello", "text_2": "bye"}, "en", ["es", "fr"]
        )

        assert deepl_provider.text_to_translate == {"text_1": "hello", "text_2": "bye"}
        assert list(deepl_provider.translation.keys()) == ["es", "fr"]
        assert list(deepl_provider.translation["es"].keys()) == ["text_1", "text_2"]
        assert list(deepl_provider.translation["fr"].keys()) == ["text_1", "text_2"]
        assert deepl_provider.translation["es"] == {"text_1": "hola", "text_2": "adiós"}
        assert deepl_provider.translation["fr"] == {
            "text_1": "Bonjour",
            "text_2": "au revoir",
        }
        assert translation == {
            "es": {"text_1": "hola", "text_2": "adiós"},
            "fr": {"text_1": "Bonjour", "text_2": "au revoir"},
        }

    def test_language_not_found_doesnt_stop_the_process(self):
        deepl_provider = Deepl()
        translation = deepl_provider.translate(
            {"text_1": "hello", "text_2": "bye"}, "en", ["es", "not_exist", "fr"]
        )

        assert deepl_provider.text_to_translate == {"text_1": "hello", "text_2": "bye"}
        assert list(deepl_provider.translation.keys()) == ["es", "fr"]
        assert list(deepl_provider.translation["es"].keys()) == ["text_1", "text_2"]
        assert list(deepl_provider.translation["fr"].keys()) == ["text_1", "text_2"]
        assert deepl_provider.translation["es"] == {"text_1": "hola", "text_2": "adiós"}
        assert deepl_provider.translation["fr"] == {
            "text_1": "Bonjour",
            "text_2": "au revoir",
        }
        assert translation == {
            "es": {"text_1": "hola", "text_2": "adiós"},
            "fr": {"text_1": "Bonjour", "text_2": "au revoir"},
        }

    def test_translation_text_incldes_hidden_values(self):
        deepl_provider = Deepl()
        translation = deepl_provider.translate(
            {
                "Hello": "hello",
                "morning": {":attribute": ["good morning ", " see you later!"]},
                "Bye": "bye",
            },
            "en",
            ["es", "fr"],
        )

        assert deepl_provider.text_to_translate == {
            "Hello": "hello",
            "morning": {":attribute": ["good morning ", " see you later!"]},
            "Bye": "bye",
        }
        assert list(deepl_provider.translation.keys()) == ["es", "fr"]
        assert list(deepl_provider.translation["es"].keys()) == [
            "Hello",
            "morning",
            "Bye",
        ]
        assert list(deepl_provider.translation["fr"].keys()) == [
            "Hello",
            "morning",
            "Bye",
        ]

        assert deepl_provider.translation["es"] == {
            "Hello": "hola",
            "morning": "buenos días :attribute ¡hasta luego!",
            "Bye": "adiós",
        }
        assert deepl_provider.translation["fr"] == {
            "Hello": "Bonjour",
            "morning": "bonjour :attribute à plus tard !",
            "Bye": "au revoir",
        }
        assert translation == {
            "es": {
                "Hello": "hola",
                "morning": "buenos días :attribute ¡hasta luego!",
                "Bye": "adiós",
            },
            "fr": {
                "Hello": "Bonjour",
                "morning": "bonjour :attribute à plus tard !",
                "Bye": "au revoir",
            },
        }
