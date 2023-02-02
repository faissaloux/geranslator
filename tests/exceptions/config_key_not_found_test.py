from geranslator.exceptions.ConfigKeyNotFound import ConfigKeyNotFound

class TestConfigKeyNotFoundException:

    def test_exception_attributes(self):
        exception = ConfigKeyNotFound('not_found')
        assert exception.key == 'not_found'

    def test_exception_message(self):
        exception = ConfigKeyNotFound('not_found')
        assert all(text in str(exception) for text in ['not_found', 'not found in config file'])
