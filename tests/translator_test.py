from geranslator.translator.translator import Translator
from geranslator.languages.languages import Languages

class TestTranslator:

    def test_set_translator_from_lang(self):
        translator = Translator().from_lang('en')

        assert isinstance(translator.lang_from_file, str)
        assert translator.lang_from_file == Languages().get('en')

    def test_set_translator_one_to_lang(self):
        translator = Translator().to_lang('ar')

        assert isinstance(translator.lang_to_files, list)
        assert translator.lang_to_files == [Languages().get('ar')]

    def test_set_translator_multiple_to_langs_using_array(self):
        translator = Translator().to_lang(['ar', 'fr'])

        assert isinstance(translator.lang_to_files, list)
        assert translator.lang_to_files == [Languages().get('ar'), Languages().get('fr')]

    def test_set_translator_multiple_to_langs_without_using_array(self):
        translator = Translator().to_lang('ar', 'fr')

        assert isinstance(translator.lang_to_files, list)
        assert translator.lang_to_files == [Languages().get('ar'), Languages().get('fr')]
