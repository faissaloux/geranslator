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