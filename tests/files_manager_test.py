import os
import pytest
import shutil

from geranslator.files_manager.files_manager import FilesManager
from geranslator.config.config import Config

@pytest.fixture(autouse=True)
def before_and_after_test():
    
    lang_dir = Config().get('lang_dir')

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/english.json", 'w')
    lang_file.write('{"Hello": "hello", "Bye": "bye"}')
    lang_file.close()

    yield
    
    shutil.rmtree(lang_dir)

class TestFilesManager:

    def test_set_extension(self):
        files_manager = FilesManager()
        files_manager.set_extension('json')

        assert files_manager.extension == 'json'

    def test_set_data(self):
        files_manager = FilesManager()
        files_manager.set_data({'Hello': 'Bonjour', 'Bye': 'Au revoir'})

        assert files_manager.data == {'Hello': 'Bonjour', 'Bye': 'Au revoir'}

    def test_set_lang(self):
        files_manager = FilesManager()
        files_manager.set_lang('english')

        assert files_manager.lang == 'english'

    def test_data_insertion_default_extension(self):
        FilesManager().set_data({'Hello': 'Bonjour', 'Bye': 'Au revoir'}).set_lang('english').insert()

        assert os.path.exists(os.path.join(os.getcwd(), Config().get('lang_dir'), 'english.' + Config().get('lang_files_ext')))

    def test_data_insertion(self):
        FilesManager().set_data({'Hello': 'Bonjour', 'Bye': 'Au revoir'}).set_lang('english').set_extension('json').insert()

        assert os.path.exists(os.path.join(os.getcwd(), Config().get('lang_dir'), 'english.json'))

    def test_get_keys(self):
        keys = FilesManager().set_lang('english').get_keys()

        assert keys == ['Hello', 'Bye']
