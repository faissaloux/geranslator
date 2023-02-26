import os
import shutil

import pytest

from geranslator.config.config import Config
from geranslator.exceptions.MissingExtension import MissingExtension
from geranslator.exceptions.MissingOriginLang import MissingOriginLang
from geranslator.exceptions.MissingProvider import MissingProvider
from geranslator.exceptions.MissingTargetLang import MissingTargetLang
from geranslator.exceptions.OriginLangFileNotFound import OriginLangFileNotFound
from geranslator.geranslator import Geranslator


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


class TestGeranslator:
    def test_default_lang_dir(self):
        geranslator = Geranslator()

        assert geranslator.lang_dir == os.path.join(
            os.getcwd(), Config().get("lang_dir")
        )

    def test_default_lang_files_extension(self):
        geranslator = Geranslator()

        assert geranslator.lang_files_ext == Config().get("lang_files_ext")

    def test_default_provider(self):
        geranslator = Geranslator()

        assert geranslator.provider == Config().get("provider")

    def test_set_provider(self):
        geranslator = Geranslator()
        geranslator.set_provider("google")

        assert geranslator.provider == "google"

    def test_set_empty_provider(self):
        with pytest.raises(MissingProvider):
            Geranslator().set_provider("")

    def test_set_lang_dir(self):
        geranslator = Geranslator()
        geranslator.set_lang_dir("translations")

        assert geranslator.lang_dir == os.path.join(os.getcwd(), "translations")

    def test_set_origin_lang(self):
        geranslator = Geranslator()
        geranslator.set_origin_lang("en")

        assert geranslator.origin_lang == "en"

    def test_set_empty_origin_lang(self):
        with pytest.raises(MissingOriginLang):
            Geranslator().set_origin_lang("")

    def test_set_one_target_lang(self):
        geranslator = Geranslator()
        geranslator.set_target_lang("en")

        assert geranslator.target_lang == ["en"]

    def test_set_multiple_target_langs(self):
        geranslator = Geranslator()
        geranslator.set_target_lang("en", "ar")

        assert geranslator.target_lang == ["en", "ar"]

    def test_set_empty_target_lang(self):
        geranslator = Geranslator()
        geranslator.set_target_lang("en", "", "ar")

        assert geranslator.target_lang == ["en", "ar"]

    def test_set_empty_target_langs(self):
        with pytest.raises(MissingTargetLang):
            Geranslator().set_target_lang("")

    def test_set_multiple_target_langs_as_array(self):
        geranslator = Geranslator()
        geranslator.set_target_lang(["en", "ar"])

        assert geranslator.target_lang == ["en", "ar"]

    def test_set_lang_files_extension(self):
        geranslator = Geranslator()
        geranslator.set_lang_files_extension("po")

        assert geranslator.lang_files_ext == "po"

    def test_case_unsensitivity_lang_files_extension(self):
        geranslator = Geranslator()
        geranslator.set_lang_files_extension("JSON")

        assert geranslator.lang_files_ext == "json"

    def test_set_empty_lang_files_extension(self):
        with pytest.raises(MissingExtension):
            Geranslator().set_lang_files_extension("")

    def test_make_sure_existing_origin_lang_file_exist(self):
        geranslator = Geranslator()
        geranslator.set_lang_dir("lang")

        geranslator.make_sure_origin_lang_file_exists()

    def test_make_sure_unexisting_origin_lang_file_unexist(self):
        geranslator = Geranslator()
        geranslator.set_lang_dir("unexisted")

        with pytest.raises(OriginLangFileNotFound):
            geranslator.make_sure_origin_lang_file_exists()

    def test_remove_origin_lang_from_target_langs_if_exists(self):
        geranslator = Geranslator()
        geranslator.set_origin_lang("en")
        geranslator.set_target_lang("ar", "en", "es")

        geranslator.remove_origin_lang_from_target_langs_if_exists()

        assert geranslator.target_lang == ["ar", "es"]

    def test_default_translation(self):
        Geranslator().translate()

        for lang in Config().get("target_langs"):
            assert os.path.exists(
                os.path.join(
                    Config().get("lang_dir"),
                    lang + "." + Config().get("lang_files_ext"),
                )
            )

    def test_custom_translation(self):
        target_langs = ["es", "pt"]
        Geranslator().set_lang_dir("translations").set_origin_lang(
            "en"
        ).set_target_lang(target_langs).translate()

        for lang in target_langs:
            assert os.path.exists(
                os.path.join(
                    os.getcwd(),
                    "translations",
                    lang + "." + Config().get("lang_files_ext"),
                )
            )
