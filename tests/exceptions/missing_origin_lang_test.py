from geranslator.exceptions.MissingOriginLang import MissingOriginLang

class TestMissingOriginLangException:

    def test_exception_message(self):
        exception = MissingOriginLang()
        assert all(text in str(exception) for text in ['Origin language is missing'])
