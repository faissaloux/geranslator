import os
import shutil

import pytest
import yaml

from geranslator.config.config import Config
from geranslator.files_manager.extensions.yaml import Yaml


@pytest.fixture(autouse=True)
def before_and_after_test():
    lang_dir = Config().get("lang_dir")

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.yaml", "w")
    yaml.dump({"Hello": "hello", "Bye": "bye"}, lang_file, allow_unicode=True)
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)


class TestYamlExtension:
    def test_get(self):
        yaml_data = Yaml().get(os.path.join(Config().get("lang_dir"), "en.yaml"))

        assert yaml_data == {"Hello": "hello", "Bye": "bye"}

    def test_insertion(self):
        yaml_file = os.path.join(Config().get("lang_dir"), "fr.yaml")
        Yaml().insert({"Hey": "Bonjour", "Bye": "Au revoir"}, yaml_file)

        assert os.path.exists(os.path.join(os.getcwd(), yaml_file))
        assert yaml.load(open(yaml_file, "r"), Loader=yaml.Loader) == {
            "Bye": "Au revoir",
            "Hey": "Bonjour",
        }

    def test_skip_hidden(self):
        lang_dir = Config().get("lang_dir")
        lang_file = open(f"{lang_dir}/en.yaml", "w")
        lang_file.write(
            '{"Hello": "hello", "morning": "good morning %attribute% , see you later!","Bye": "bye"}'
        )
        lang_file.close()

        yaml_data = Yaml().get(os.path.join(Config().get("lang_dir"), "en.yaml"))
        assert yaml_data == {
            "Hello": "hello",
            "morning": {"%attribute%": ["good morning ", " , see you later!"]},
            "Bye": "bye",
        }

    def test_skip_multiple_different_hidden(self):
        lang_dir = Config().get("lang_dir")
        lang_file = open(f"{lang_dir}/en.yaml", "w")
        lang_file.write(
            '{"Hello": "hello", "morning": "good morning %attribute1% , see you %attribute2% later!","Bye": "bye"}'
        )
        lang_file.close()

        yaml_data = Yaml().get(os.path.join(Config().get("lang_dir"), "en.yaml"))
        assert yaml_data == {
            "Hello": "hello",
            "morning": {
                "%attribute1%": [
                    "good morning ",
                    {"%attribute2%": [" , see you ", " later!"]},
                ]
            },
            "Bye": "bye",
        }
