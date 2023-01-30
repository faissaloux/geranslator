from geranslator.exceptions.MissingOriginLang import MissingOriginLang

class TestMissingOriginLangException:

    def test_exception_message(self):
        exception = MissingOriginLang()
        assert all(word in str(exception) for word in ['Origin language is missing'])
