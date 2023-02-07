from geranslator.exceptions.FileNotFound import FileNotFound


class TestFileNotFoundException:
    def test_exception_attributes(self):
        exception = FileNotFound("not_found")

        assert exception.file == "not_found"

    def test_exception_message(self):
        exception = FileNotFound("not_found")

        assert all(text in str(exception) for text in ["not_found", "file not found"])
