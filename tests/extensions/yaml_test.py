import os
import pytest
import shutil
import yaml

from geranslator.config.config import Config
from geranslator.files_manager.extensions.yaml import Yaml

@pytest.fixture(autouse=True)
def before_and_after_test():

    lang_dir = Config().get('lang_dir')

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.yaml", 'w')
    yaml.dump({"Hello": "hello", "Bye": "bye"}, lang_file, allow_unicode = True)
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)

class TestYamlExtension:

    def test_get_keys(self):
        json_keys = Yaml().get_keys(os.path.join(Config().get('lang_dir'), 'en.yaml'))

        assert json_keys == ['Bye', 'Hello']

    def test_insertion(self):
        yaml_file = os.path.join(Config().get('lang_dir'), 'fr.yaml')
        Yaml().insert({"Hey": "Bonjour", "Bye": "Au revoir"}, yaml_file)


        assert yaml.load(open(yaml_file, "r"), Loader=yaml.Loader) == {'Bye': 'Au revoir', 'Hey': 'Bonjour'}
