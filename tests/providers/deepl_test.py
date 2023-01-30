import os
import pytest
import shutil

from geranslator.config.config import Config
from geranslator.provider.providers.deepl import Deepl

@pytest.fixture(autouse=True)
def before_and_after_test():

    lang_dir = Config().get('lang_dir')

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.json", 'w')
    lang_file.write('{"Hello": "hello", "Bye": "bye"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)

class TestDeeplProvider:

    def test_url(self):
        assert Deepl().url == 'https://www.deepl.com/translator'

    def test_words_to_translate(self):
        deepl_provider = Deepl()
        deepl_provider.translate(['Hello', 'Bye'], 'en', ['es', 'fr'])

        assert deepl_provider.words_to_translate == ['Hello', 'Bye']

    def test_translation_words(self):
        deepl_provider = Deepl()
        translation = deepl_provider.translate(['Hello', 'Bye'], 'en', ['es', 'fr'])

        assert list(deepl_provider.translation.keys()) == ['es', 'fr']
        assert list(deepl_provider.translation['es'].keys()) == ['Hello', 'Bye']
        assert list(deepl_provider.translation['fr'].keys()) == ['Hello', 'Bye']
        assert deepl_provider.translation['es'] == {'Hello': 'Hola', 'Bye': 'Adiós'}
        assert deepl_provider.translation['fr'] == {'Hello': 'Bonjour', 'Bye': 'Au revoir'}
        assert translation == {'es': {'Hello': 'Hola', 'Bye': 'Adiós'}, 'fr': {'Hello': 'Bonjour', 'Bye': 'Au revoir'}}

    def test_language_not_found_doesnt_stop_the_process(self):
        deepl_provider = Deepl()
        translation = deepl_provider.translate(['Hello', 'Bye'], 'en', ['es', 'not_exist', 'fr'])

        assert list(deepl_provider.translation.keys()) == ['es', 'fr']
        assert list(deepl_provider.translation['es'].keys()) == ['Hello', 'Bye']
        assert list(deepl_provider.translation['fr'].keys()) == ['Hello', 'Bye']
        assert deepl_provider.translation['es'] == {'Hello': 'Hola', 'Bye': 'Adiós'}
        assert deepl_provider.translation['fr'] == {'Hello': 'Bonjour', 'Bye': 'Au revoir'}
        assert translation == {'es': {'Hello': 'Hola', 'Bye': 'Adiós'}, 'fr': {'Hello': 'Bonjour', 'Bye': 'Au revoir'}}
