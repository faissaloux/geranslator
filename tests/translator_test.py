import os
import pytest
import shutil

from geranslator.config.config import Config
from geranslator.translator.translator import Translator

@pytest.fixture(autouse=True)
def before_and_after_test():

    lang_dir = Config().get('lang_dir')

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.json", 'w')
    lang_file.write('{"Hey": "hey"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)

class TestTranslator:

    def test_set_translator_from_lang(self):
        translator = Translator().from_lang('en')

        assert isinstance(translator.lang_from_file, str)
        assert translator.lang_from_file == 'en'

    def test_set_translator_one_to_lang(self):
        translator = Translator().to_lang('ar')

        assert isinstance(translator.lang_to_files, list)
        assert translator.lang_to_files == ['ar']

    def test_set_translator_multiple_to_langs_using_array(self):
        translator = Translator().to_lang(['ar', 'fr'])

        assert isinstance(translator.lang_to_files, list)
        assert translator.lang_to_files == ['ar', 'fr']

    def test_set_translator_multiple_to_langs_without_using_array(self):
        translator = Translator().to_lang('ar', 'fr')

        assert isinstance(translator.lang_to_files, list)
        assert translator.lang_to_files == ['ar', 'fr']

    def test_translation(self):
        target_langs = ['es', 'pt']
        Translator().from_lang('en').to_lang(target_langs).translate()

        for lang in target_langs:
            assert os.path.exists(os.path.join(Config().get('lang_dir'), lang + '.' + Config().get('lang_files_ext')))
