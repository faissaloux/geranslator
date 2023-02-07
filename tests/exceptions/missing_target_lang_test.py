from geranslator.exceptions.MissingTargetLang import MissingTargetLang


class TestMissingTargetLangException:
    def test_exception_message(self):
        exception = MissingTargetLang()
        assert all(text in str(exception) for text in ["Target languages are missing"])
