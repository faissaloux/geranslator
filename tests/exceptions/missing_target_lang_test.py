from geranslator.exceptions.MissingTargetLang import MissingTargetLang

class TestMissingTargetLangException:

    def test_exception_message(self):
        exception = MissingTargetLang()
        assert all(word in str(exception) for word in ['Target languages are missing'])
