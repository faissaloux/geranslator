from geranslator.exceptions.MissingExtension import MissingExtension

class TestMissingExtensionException:

    def test_exception_message(self):
        exception = MissingExtension()
        assert all(word in str(exception) for word in ['Extension is missing'])
