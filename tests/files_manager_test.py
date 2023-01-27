import os
import pytest
import shutil

from geranslator.files_manager.files_manager import FilesManager
from geranslator.config.config import Config

@pytest.fixture(autouse=True)
def before_and_after_test():

    lang_dirs = [
        Config().get('lang_dir'),
        'translations'
    ]

    for lang_dir in lang_dirs:
        os.mkdir(lang_dir)
        lang_file = open(f"{lang_dir}/en.json", 'w')
        lang_file.write('{"Hello": "hello", "Bye": "bye"}')
        lang_file.close()

    yield

    for lang_dir in lang_dirs:
        shutil.rmtree(lang_dir)

class TestFilesManager:

    def test_set_extension(self):
        files_manager = FilesManager()
        files_manager.set_extension('json')

        assert files_manager.extension == 'json'

    def test_supported_extensions(self):
        supported_extensions = [
            'json',
            'yaml'
        ]

        for extension in supported_extensions:
            files_manager = FilesManager()
            files_manager.set_extension(extension)

            assert files_manager.extension == extension

    def test_set_data(self):
        files_manager = FilesManager()
        files_manager.set_data({'Hello': 'Bonjour', 'Bye': 'Au revoir'})

        assert files_manager.data == {'Hello': 'Bonjour', 'Bye': 'Au revoir'}

    def test_set_lang(self):
        files_manager = FilesManager()
        files_manager.set_lang('en')

        assert files_manager.lang == 'en'

    def test_set_dir(self):
        files_manager = FilesManager()
        files_manager.set_dir('translations')

        assert files_manager.dir == 'translations'

    def test_data_insertion_default_extension(self):
        FilesManager().set_data({'Hello': 'Bonjour', 'Bye': 'Au revoir'}).set_lang('en').insert()

        assert os.path.exists(os.path.join(os.getcwd(), Config().get('lang_dir'), 'en.' + Config().get('lang_files_ext')))

    def test_data_insertion(self):
        FilesManager().set_dir('translations').set_data({'Hello': 'Bonjour', 'Bye': 'Au revoir'}).set_lang('en').set_extension('json').insert()

        assert os.path.exists(os.path.join(os.getcwd(), 'translations', 'en.json'))

    def test_get_keys(self):
        keys = FilesManager().set_lang('en').get_keys()

        assert keys == ['Hello', 'Bye']
