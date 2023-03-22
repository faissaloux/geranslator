import os
import shutil

import pytest
import yaml

from geranslator.config.config import Config
from geranslator.geranslator import Geranslator


@pytest.fixture(autouse=True)
def before_and_after_test():
    lang_dir = Config().get("lang_dir")

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/messages.en.yaml", "w")
    yaml.dump({"Hello": "hello", "Bye": "bye"}, lang_file, allow_unicode=True)
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)


class TestGeranslatorPrefixedFilesNamesTest:
    def test_default_translation(self):
        Geranslator().set_lang_files_extension("yaml").translate()

        for lang in Config().get("target_langs"):
            assert os.path.exists(
                os.path.join(
                    Config().get("lang_dir"),
                    "messages." + lang + ".yaml",
                )
            )
