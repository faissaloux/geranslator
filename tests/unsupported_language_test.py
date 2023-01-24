from geranslator.exceptions.UnsupportedLanguage import UnsupportedLanguage

class TestUnsupportedLanguageException:

    def test_exception_attributes(self):
        exception = UnsupportedLanguage('not_supported')
        assert exception.language == 'not_supported'

    def test_exception_message(self):
        exception = UnsupportedLanguage('not_supported')
        assert all(word in str(exception) for word in ['not_supported', 'language not supported'])
