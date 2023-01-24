import os
import pytest
import shutil

from geranslator.config.config import Config
from geranslator.provider.providers.google import Google

@pytest.fixture(autouse=True)
def before_and_after_test():

    lang_dir = Config().get('lang_dir')

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/english.json", 'w')
    lang_file.write('{"Hello": "hello", "Bye": "bye"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)

class TestGoogleProvider:

    def test_url(self):
        google_provider = Google()
        google_provider.translate('english', ['arabic', 'french'])

        assert google_provider.url == 'https://translate.google.com'

    def test_words_to_translate(self):
        google_provider = Google()
        google_provider.translate('english', ['arabic', 'french'])

        assert google_provider.to_translate == ['Hello', 'Bye']

    def test_translated_words(self):
        google_provider = Google()
        google_provider.translate('english', ['arabic', 'french'])

        assert list(google_provider.translated.keys()) == ['arabic', 'french']
        assert list(google_provider.translated['arabic'].keys()) == ['Hello', 'Bye']
        assert list(google_provider.translated['french'].keys()) == ['Hello', 'Bye']
        assert google_provider.translated['arabic'] == {'Hello': 'مرحبًا', 'Bye': 'وداعا'}
        assert google_provider.translated['french'] == {'Hello': 'Bonjour', 'Bye': 'Au revoir'}
