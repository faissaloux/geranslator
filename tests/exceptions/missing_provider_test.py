from geranslator.exceptions.MissingProvider import MissingProvider

class TestMissingProviderException:

    def test_exception_message(self):
        exception = MissingProvider()
        assert all(text in str(exception) for text in ['Provider is missing'])
