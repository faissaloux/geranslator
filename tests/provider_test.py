import os
import pytest
import shutil

from geranslator.config.config import Config
from geranslator.provider.provider import Provider
from geranslator.exceptions.ProviderNotFound import ProviderNotFound

@pytest.fixture(autouse=True)
def before_and_after_test():

    lang_dir = Config().get('lang_dir')

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.json", 'w')
    lang_file.write('{"Hey": "hey"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)

class TestProvider:

    def test_set_provider(self):
        provider = Provider()
        provider.set_provider('google')

        assert provider.provider == 'google'

    def test_make_sure_existing_provider_exist(self):
        provider = Provider()
        provider.set_provider('google')

        provider.make_sure_provider_exists()

    def test_make_sure_unexisting_provider_unexist(self):
        provider = Provider()
        provider.set_provider('unexisted')

        with pytest.raises(ProviderNotFound):
            provider.make_sure_provider_exists()

    def test_translation(self):
        target_langs = ['es', 'pt']
        Provider().translate('en', target_langs)

        for lang in target_langs:
            assert os.path.exists(os.path.join(Config().get('lang_dir'), lang + '.' + Config().get('lang_files_ext')))
