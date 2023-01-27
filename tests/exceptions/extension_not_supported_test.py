from geranslator.exceptions.ExtensionNotSupported import ExtensionNotSupported

class TestExtensionNotSupportedException:

    def test_exception_attributes(self):
        exception = ExtensionNotSupported('pdf')
        assert exception.extension == 'pdf'

    def test_exception_message(self):
        exception = ExtensionNotSupported('pdf')
        assert all(word in str(exception) for word in ['pdf', 'file format not supported'])
