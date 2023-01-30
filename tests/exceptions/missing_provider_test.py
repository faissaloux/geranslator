from geranslator.exceptions.MissingProvider import MissingProvider

class TestMissingProviderException:

    def test_exception_message(self):
        exception = MissingProvider()
        assert all(word in str(exception) for word in ['Provider is missing'])
