import json
import os
import shutil

import pytest

from geranslator.config.config import Config
from geranslator.files_manager.extensions.json import Json


@pytest.fixture(autouse=True)
def before_and_after_test():
    lang_dir = Config().get("lang_dir")

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.json", "w")
    lang_file.write('{"Hello": "hello", "Bye": "bye"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)


class TestJsonExtension:
    def test_hidden_value(self):
        assert Json().hidden == ["^:"]

    def test_get(self):
        json_data = Json().get(os.path.join(Config().get("lang_dir"), "en.json"))

        assert json_data == {"Hello": "hello", "Bye": "bye"}

    def test_insertion(self):
        json_file = os.path.join(Config().get("lang_dir"), "fr.json")
        Json().insert({"Hey": "Bonjour", "Bye": "Au revoir"}, json_file)

        assert os.path.exists(os.path.join(os.getcwd(), json_file))
        assert json.load(open(json_file, "r")) == {"Hey": "Bonjour", "Bye": "Au revoir"}

    def test_prevent_override(self):
        json_file = os.path.join(Config().get("lang_dir"), "fr.json")
        lang_file = open(json_file, "w")
        lang_file.write('{"Hey": "Bonjour"}')
        lang_file.close()

        Json().insert({"Bye": "Au revoir"}, json_file)

        assert os.path.exists(os.path.join(os.getcwd(), json_file))
        assert json.load(open(json_file, "r")) == {"Hey": "Bonjour", "Bye": "Au revoir"}

    def test_skip_hidden(self):
        lang_dir = Config().get("lang_dir")
        lang_file = open(f"{lang_dir}/en.json", "w")
        lang_file.write(
            '{"Hello": "hello", "morning": "good morning :attribute , see you later!","Bye": "bye"}'
        )
        lang_file.close()

        json_data = Json().get(os.path.join(Config().get("lang_dir"), "en.json"))
        assert json_data == {
            "Hello": "hello",
            "morning": {":attribute": ["good morning ", " , see you later!"]},
            "Bye": "bye",
        }

    def test_skip_multiple_same_hidden(self):
        lang_dir = Config().get("lang_dir")
        lang_file = open(f"{lang_dir}/en.json", "w")
        lang_file.write(
            '{"Hello": "hello", "morning": "good morning :attribute , see you :attribute later!","Bye": "bye"}'
        )
        lang_file.close()

        json_data = Json().get(os.path.join(Config().get("lang_dir"), "en.json"))
        assert json_data == {
            "Hello": "hello",
            "morning": {":attribute": ["good morning ", " , see you ", " later!"]},
            "Bye": "bye",
        }

    def test_skip_multiple_different_hidden(self):
        lang_dir = Config().get("lang_dir")
        lang_file = open(f"{lang_dir}/en.json", "w")
        lang_file.write(
            '{"Hello": "hello", "morning": "good morning :attribute1 , see you :attribute2 later!","Bye": "bye"}'
        )
        lang_file.close()

        json_data = Json().get(os.path.join(Config().get("lang_dir"), "en.json"))
        assert json_data == {
            "Hello": "hello",
            "morning": {
                ":attribute1": [
                    "good morning ",
                    {":attribute2": [" , see you ", " later!"]},
                ]
            },
            "Bye": "bye",
        }
