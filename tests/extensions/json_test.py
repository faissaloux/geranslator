import os
import pytest
import shutil
import json

from geranslator.config.config import Config
from geranslator.files_manager.extensions.json import Json

@pytest.fixture(autouse=True)
def before_and_after_test():

    lang_dir = Config().get('lang_dir')

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.json", 'w')
    lang_file.write('{"Hello": "hello", "Bye": "bye"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)

class TestJsonExtension:

    def test_get_keys(self):
        json_keys = Json().get_keys(os.path.join(Config().get('lang_dir'), 'en.json'))

        assert json_keys == ['Hello', 'Bye']

    def test_insertion(self):
        json_file = os.path.join(Config().get('lang_dir'), 'fr.json')
        Json().insert({"Hey": "Bonjour", "Bye": "Au revoir"}, json_file)

        assert json.load(open(json_file, "r")) == {"Hey": "Bonjour", "Bye": "Au revoir"}
