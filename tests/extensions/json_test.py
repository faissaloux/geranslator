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
    def test_get(self):
        json_keys = Json().get(os.path.join(Config().get("lang_dir"), "en.json"))

        assert json_keys == {"Hello": "hello", "Bye": "bye"}

    def test_insertion(self):
        json_file = os.path.join(Config().get("lang_dir"), "fr.json")
        Json().insert({"Hey": "Bonjour", "Bye": "Au revoir"}, json_file)

        assert os.path.exists(os.path.join(os.getcwd(), json_file))
        assert json.load(open(json_file, "r")) == {"Hey": "Bonjour", "Bye": "Au revoir"}
