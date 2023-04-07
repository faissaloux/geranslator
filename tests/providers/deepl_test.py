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
    lang_file.write('{"text_1": "two", "text_2": "three"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)


class TestDeeplProvider:
    def test_url(self):
        assert Deepl().url == "https://www.deepl.com/translator"

    def test_exit_when_origin_lang_is_not_supported(self):
        with pytest.raises(SystemExit):
            Deepl().translate(
                {"text_1": "two", "text_2": "three"},
                "not_supported",
                ["ar", "fr"],
                Config().get("lang_dir"),
                "json",
            )

    def test_translation_text(self):
        deepl_provider = Deepl()
        translation = deepl_provider.translate(
            {"text_1": "two", "text_2": "three"},
            "en",
            ["es", "fr"],
            Config().get("lang_dir"),
            "json",
        )

        assert deepl_provider.text_to_translate == {"text_1": "two", "text_2": "three"}
        assert list(deepl_provider.translation.keys()) == ["es", "fr"]
        assert list(deepl_provider.translation["es"].keys()) == ["text_1", "text_2"]
        assert list(deepl_provider.translation["fr"].keys()) == ["text_1", "text_2"]
        assert translation == deepl_provider.translation
        assert translation == {
            "es": {"text_1": "dos", "text_2": "tres"},
            "fr": {"text_1": "deux", "text_2": "trois"},
        }

    def test_translation_returns_lower_case(self):
        deepl_provider = Deepl()
        translation = deepl_provider.translate(
            {"text_1": "TWO", "text_2": "THREE"},
            "en",
            ["es", "fr"],
            Config().get("lang_dir"),
            "json",
        )

        assert translation == {
            "es": {"text_1": "dos", "text_2": "tres"},
            "fr": {"text_1": "deux", "text_2": "trois"},
        }

    def test_language_not_found_doesnt_stop_the_process(self):
        deepl_provider = Deepl()
        translation = deepl_provider.translate(
            {"text_1": "two", "text_2": "three"},
            "en",
            ["es", "not_exist", "fr"],
            Config().get("lang_dir"),
            "json",
        )

        assert deepl_provider.text_to_translate == {"text_1": "two", "text_2": "three"}
        assert list(deepl_provider.translation.keys()) == ["es", "fr"]
        assert list(deepl_provider.translation["es"].keys()) == ["text_1", "text_2"]
        assert list(deepl_provider.translation["fr"].keys()) == ["text_1", "text_2"]
        assert translation == deepl_provider.translation
        assert translation == {
            "es": {"text_1": "dos", "text_2": "tres"},
            "fr": {"text_1": "deux", "text_2": "trois"},
        }

    def test_translation_text_includes_hidden_value(self):
        deepl_provider = Deepl()
        translation = deepl_provider.translate(
            {
                "Hello": "hello",
                "morning": {":attribute": ["good morning ", " have a good day"]},
                "Bye": "bye",
            },
            "en",
            ["es", "sv"],
            Config().get("lang_dir"),
            "json",
        )

        assert deepl_provider.text_to_translate == {
            "Hello": "hello",
            "morning": {":attribute": ["good morning ", " have a good day"]},
            "Bye": "bye",
        }
        assert list(deepl_provider.translation.keys()) == ["es", "sv"]
        assert list(deepl_provider.translation["es"].keys()) == [
            "Hello",
            "morning",
            "Bye",
        ]
        assert list(deepl_provider.translation["sv"].keys()) == [
            "Hello",
            "morning",
            "Bye",
        ]
        assert translation == deepl_provider.translation
        assert translation == {
            "es": {
                "Hello": "hola",
                "morning": "buenos días :attribute que tenga un buen día",
                "Bye": "adiós",
            },
            "sv": {
                "Hello": "hej",
                "morning": "god morgon :attribute ha en bra dag",
                "Bye": "hej då",
            },
        }

    def test_translation_text_includes_multiple_hidden_values(self):
        deepl_provider = Deepl()
        translation = deepl_provider.translate(
            {
                "morning": {
                    ":attribute1": [
                        "good morning",
                        {":attribute2": [" , see you ", " later!"]},
                    ]
                }
            },
            "en",
            ["es", "sv"],
            Config().get("lang_dir"),
            "json",
        )

        assert deepl_provider.text_to_translate == {
            "morning": {
                ":attribute1": [
                    "good morning",
                    {":attribute2": [" , see you ", " later!"]},
                ]
            }
        }
        assert list(deepl_provider.translation.keys()) == ["es", "sv"]
        assert list(deepl_provider.translation["es"].keys()) == ["morning"]
        assert list(deepl_provider.translation["sv"].keys()) == ["morning"]
        assert translation == deepl_provider.translation
        assert translation == {
            "es": {
                "morning": "buenos días:attribute1 nos vemos. :attribute2 ¡más tarde!"
            },
            "sv": {"morning": "god morgon:attribute1 , vi ses :attribute2 senare!"},
        }
