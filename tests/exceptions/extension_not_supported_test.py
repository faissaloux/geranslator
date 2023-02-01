from geranslator.exceptions.ExtensionNotSupported import ExtensionNotSupported

class TestExtensionNotSupportedException:

    def test_exception_attributes(self):
        exception = ExtensionNotSupported('pdf')
        assert exception.extension == 'pdf'

    def test_exception_message(self):
        exception = ExtensionNotSupported('pdf')
        assert all(text in str(exception) for text in ['pdf', 'file format not supported'])
