from geranslator.exceptions.OriginLangFileNotFound import OriginLangFileNotFound

class TestOriginLangFileNotFoundException:

    def test_exception_attributes(self):
        exception = OriginLangFileNotFound('unexisted.json')
        assert exception.origin_lang_file == 'unexisted.json'

    def test_exception_message(self):
        exception = OriginLangFileNotFound('unexisted.json')
        assert all(word in str(exception) for word in ['unexisted.json', 'not found'])
