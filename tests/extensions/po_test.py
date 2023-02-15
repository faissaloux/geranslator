import os
import shutil

import polib
import pytest

from geranslator.config.config import Config
from geranslator.files_manager.extensions.po import Po


@pytest.fixture(autouse=True)
def before_and_after_test():
    lang_dir = Config().get("lang_dir")

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.po", "w")
    lang_file.write("msgid 'Hello'\n msgstr 'hello'\n\n msgid 'Bye'\n msgstr 'bye'")
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)


class TestPoExtension:
    def test_get(self):
        po_data = Po().get(os.path.join(Config().get("lang_dir"), "en.po"))

        assert po_data == {"Hello": "hello", "Bye": "bye"}

    def test_insertion(self):
        po_file = os.path.join(Config().get("lang_dir"), "fr.po")
        Po().insert({"Hello": "Bonjour", "Bye": "Au revoir"}, po_file)

        assert os.path.exists(os.path.join(os.getcwd(), po_file))
        assert (
            str(polib.pofile(po_file))
            == """#
msgid ""
msgstr ""

msgid "Hello"
msgstr "Bonjour"

msgid "Bye"
msgstr "Au revoir"
"""
        )

    def test_skip_hidden(self):
        lang_dir = Config().get("lang_dir")
        lang_file = open(f"{lang_dir}/en.po", "w")
        lang_file.write(
            "msgid 'Hello'\n msgstr 'hello'\n\n msgid 'morning'\n msgstr 'good morning %attribute , see you later!'\n\n msgid 'Bye'\n msgstr 'bye'"
        )
        lang_file.close()

        po_data = Po().get(os.path.join(Config().get("lang_dir"), "en.po"))
        assert po_data == {
            "Hello": "hello",
            "morning": {"%attribute": ["good morning ", " , see you later!"]},
            "Bye": "bye",
        }
