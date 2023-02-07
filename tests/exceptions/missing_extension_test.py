from geranslator.exceptions.MissingExtension import MissingExtension


class TestMissingExtensionException:
    def test_exception_message(self):
        exception = MissingExtension()
        assert all(text in str(exception) for text in ["Extension is missing"])
