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
    lang_file.write('{"text_1": "hello", "text_2": "bye"}')
    lang_file.close()

    yield

    shutil.rmtree(lang_dir)

class TestGoogleProvider:

    def test_url(self):
        assert Google().url == 'https://translate.google.com'

    def test_translation_text(self):
        google_provider = Google()
        translation = google_provider.translate({"text_1": "hello", "text_2": "bye"}, 'en', ['ar', 'fr'])

        assert google_provider.text_to_translate == {"text_1": "hello", "text_2": "bye"}
        assert list(google_provider.translation.keys()) == ['ar', 'fr']
        assert list(google_provider.translation['ar'].keys()) == ['text_1', 'text_2']
        assert list(google_provider.translation['fr'].keys()) == ['text_1', 'text_2']
        assert google_provider.translation['ar'] == {'text_1': 'أهلا', 'text_2': 'وداعا'}
        assert google_provider.translation['fr'] == {'text_1': 'salut', 'text_2': 'au revoir'}
        assert translation == {'ar': {'text_1': 'أهلا', 'text_2': 'وداعا'}, 'fr': {'text_1': 'salut', 'text_2': 'au revoir'}}

    def test_language_not_found_doesnt_stop_the_process(self):
        google_provider = Google()
        translation = google_provider.translate({"text_1": "hello", "text_2": "bye"}, 'en', ['ar', 'not_exist', 'fr'])

        assert google_provider.text_to_translate == {"text_1": "hello", "text_2": "bye"}
        assert list(google_provider.translation.keys()) == ['ar', 'fr']
        assert list(google_provider.translation['ar'].keys()) == ['text_1', 'text_2']
        assert list(google_provider.translation['fr'].keys()) == ['text_1', 'text_2']
        assert google_provider.translation['ar'] == {'text_1': 'أهلا', 'text_2': 'وداعا'}
        assert google_provider.translation['fr'] == {'text_1': 'salut', 'text_2': 'au revoir'}
        assert translation == {'ar': {'text_1': 'أهلا', 'text_2': 'وداعا'}, 'fr': {'text_1': 'salut', 'text_2': 'au revoir'}}
