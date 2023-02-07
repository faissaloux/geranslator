from geranslator.exceptions.ProviderNotFound import ProviderNotFound


class TestProviderNotFoundException:
    def test_exception_attributes(self):
        exception = ProviderNotFound("not_found")
        assert exception.provider == "not_found"

    def test_exception_message(self):
        exception = ProviderNotFound("not_found")
        assert all(
            text in str(exception) for text in ["not_found", "provider not found"]
        )
