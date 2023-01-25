import os
import pytest
import shutil

from geranslator.geranslator import Geranslator
from geranslator.config.config import Config
from geranslator.exceptions.OriginLangFileNotFound import OriginLangFileNotFound

@pytest.fixture(autouse=True)
def before_and_after_test():

    lang_dir = Config().get('lang_dir')

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.json", 'w')
    lang_file.write('{"Hey": "hey"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)

class TestGeranslator:

    def test_default_lang_dir(self):
        geranslator = Geranslator()

        assert geranslator.lang_dir == os.path.join(os.getcwd(), Config().get('lang_dir'))

    def test_default_lang_files_extension(self):
        geranslator = Geranslator()

        assert geranslator.lang_files_ext == Config().get('lang_files_ext')

    def test_set_lang_dir(self):
        geranslator = Geranslator()
        geranslator.set_lang_dir('lang')

        assert geranslator.lang_dir == os.path.join(os.getcwd(), 'lang')

    def test_set_origin_lang(self):
        geranslator = Geranslator()
        geranslator.set_origin_lang('en')

        assert geranslator.origin_lang == 'en'

    def test_set_one_target_lang(self):
        geranslator = Geranslator()
        geranslator.set_target_lang('en')

        assert geranslator.target_lang == ['en']

    def test_set_multiple_target_langs(self):
        geranslator = Geranslator()
        geranslator.set_target_lang('en', 'ar')

        assert geranslator.target_lang == ['en', 'ar']

    def test_set_multiple_target_langs_as_array(self):
        geranslator = Geranslator()
        geranslator.set_target_lang(['en', 'ar'])

        assert geranslator.target_lang == ['en', 'ar']

    def test_set_lang_files_extension(self):
        geranslator = Geranslator()
        geranslator.set_lang_files_extension('po')

        assert geranslator.lang_files_ext == 'po'

    def test_make_sure_existing_origin_lang_file_exist(self):
        geranslator = Geranslator()
        geranslator.set_lang_dir('lang')

        geranslator.make_sure_origin_lang_file_exists()

    def test_make_sure_unexisting_origin_lang_file_unexist(self):
        geranslator = Geranslator()
        geranslator.set_lang_dir('unexisted')

        with pytest.raises(OriginLangFileNotFound):
            geranslator.make_sure_origin_lang_file_exists()

    def test_default_translation(self):
        Geranslator().translate()

        for lang in Config().get('to_langs'):
            assert os.path.exists(os.path.join(Config().get('lang_dir'), lang + '.' + Config().get('lang_files_ext')))

    def test_custom_translation(self):
        target_langs = ['es', 'pt']
        Geranslator().set_origin_lang('en').set_target_lang(target_langs).translate()

        for lang in ['es', 'pt']:
            assert os.path.exists(os.path.join(Config().get('lang_dir'), lang + '.' + Config().get('lang_files_ext')))
