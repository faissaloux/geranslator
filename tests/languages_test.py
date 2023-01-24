from geranslator.languages.languages import Languages

class TestLanguages:

    def test_get_existed_language(self):
        language = Languages().get('en')

        assert language == 'english'

    def test_get_unexisted_language(self):
        language = Languages().get('un')

        assert language == 'un'
