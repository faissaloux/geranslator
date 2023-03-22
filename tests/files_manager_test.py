import os
import shutil

import pytest

from geranslator.config.config import Config
from geranslator.files_manager.files_manager import FilesManager


@pytest.fixture(autouse=True)
def before_and_after_test():
    lang_dirs = [Config().get("lang_dir"), "translations"]

    for lang_dir in lang_dirs:
        os.mkdir(lang_dir)
        lang_file = open(f"{lang_dir}/en.json", "w")
        lang_file.write('{"Hello": "hello", "Bye": "bye"}')
        lang_file.close()

    yield

    for lang_dir in lang_dirs:
        shutil.rmtree(lang_dir)


class TestFilesManager:
    def test_set_extension(self):
        files_manager = FilesManager()
        files_manager.set_extension("json")

        assert files_manager.extension == "json"

    def test_supported_extensions(self):
        supported_extensions = [
            "json",
            "yaml",
            "yml",
        ]

        for extension in supported_extensions:
            files_manager = FilesManager()
            files_manager.set_extension(extension)

            assert files_manager.extension == extension

    def test_set_data(self):
        files_manager = FilesManager()
        files_manager.set_data({"Hello": "Bonjour", "Bye": "Au revoir"})

        assert files_manager.data == {"Hello": "Bonjour", "Bye": "Au revoir"}

    def test_set_lang_file(self):
        files_manager = FilesManager()
        files_manager.set_lang_file(os.path.join(Config().get("lang_dir"), "en.yaml"))

        assert files_manager.lang_file == os.path.join(
            Config().get("lang_dir"), "en.yaml"
        )

    def test_set_langs_dir(self):
        files_manager = FilesManager()
        files_manager.set_langs_dir("translations")

        assert files_manager.langs_dir == "translations"

    def test_data_insertion_default_extension(self):
        FilesManager().set_data({"Hello": "Bonjour", "Bye": "Au revoir"}).set_lang_file(
            "en"
        ).insert()

        assert os.path.exists(
            os.path.join(
                os.getcwd(),
                Config().get("lang_dir"),
                "en." + Config().get("lang_files_ext"),
            )
        )

    def test_data_insertion(self):
        FilesManager().set_langs_dir("translations").set_data(
            {"Hello": "Bonjour", "Bye": "Au revoir"}
        ).set_lang_file("en").set_extension("json").insert()

        assert os.path.exists(os.path.join(os.getcwd(), "translations", "en.json"))

    def test_get(self):
        data = (
            FilesManager()
            .set_lang_file(os.path.join(Config().get("lang_dir"), "en.json"))
            .get()
        )

        assert data == {"Hello": "hello", "Bye": "bye"}
