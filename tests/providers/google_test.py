import os
import pytest
import shutil

from geranslator.config.config import Config
from geranslator.provider.providers.google import Google

@pytest.fixture(autouse=True)
def before_and_after_test():

    lang_dir = Config().get('lang_dir')

    os.mkdir(lang_dir)
    lang_file = open(f"{lang_dir}/en.json", 'w')
    lang_file.write('{"Hello": "hello", "Bye": "bye"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)

class TestGoogleProvider:

    def test_url(self):
        assert Google().url == 'https://translate.google.com'

    def test_translation_words(self):
        google_provider = Google()
        translation = google_provider.translate(['Hello', 'Bye'], 'en', ['ar', 'fr'])

        assert google_provider.words_to_translate == ['Hello', 'Bye']
        assert list(google_provider.translation.keys()) == ['ar', 'fr']
        assert list(google_provider.translation['ar'].keys()) == ['Hello', 'Bye']
        assert list(google_provider.translation['fr'].keys()) == ['Hello', 'Bye']
        assert google_provider.translation['ar'] == {'Hello': 'مرحبًا', 'Bye': 'وداعا'}
        assert google_provider.translation['fr'] == {'Hello': 'Bonjour', 'Bye': 'Au revoir'}
        assert translation == {'ar': {'Hello': 'مرحبًا', 'Bye': 'وداعا'}, 'fr': {'Hello': 'Bonjour', 'Bye': 'Au revoir'}}

    def test_language_not_found_doesnt_stop_the_process(self):
        google_provider = Google()
        translation = google_provider.translate(['Hello', 'Bye'], 'en', ['ar', 'not_exist', 'fr'])

        assert google_provider.words_to_translate == ['Hello', 'Bye']
        assert list(google_provider.translation.keys()) == ['ar', 'fr']
        assert list(google_provider.translation['ar'].keys()) == ['Hello', 'Bye']
        assert list(google_provider.translation['fr'].keys()) == ['Hello', 'Bye']
        assert google_provider.translation['ar'] == {'Hello': 'مرحبًا', 'Bye': 'وداعا'}
        assert google_provider.translation['fr'] == {'Hello': 'Bonjour', 'Bye': 'Au revoir'}
        assert translation == {'ar': {'Hello': 'مرحبًا', 'Bye': 'وداعا'}, 'fr': {'Hello': 'Bonjour', 'Bye': 'Au revoir'}}
