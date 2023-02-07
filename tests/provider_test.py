import random
from importlib import import_module

import pytest

from geranslator.exceptions.ProviderNotFound import ProviderNotFound
from geranslator.provider.provider import Provider


class TestProvider:
    supported_providers: list = [
        "google",
        "deepl",
    ]

    def test_set_provider(self):
        provider = Provider("google")

        assert provider.provider == "google"

    def test_case_unsensitivity_provider(self):
        provider = Provider("GOOGLE")

        assert provider.provider == "google"

    def test_supported_providers(self):
        for provider in self.supported_providers:
            assert Provider(provider).provider == provider

    def test_cant_translate_using_unexisted_provider(self):
        with pytest.raises(ProviderNotFound):
            Provider("unexisted").translate(["Hello"], "en", ["ar", "fr"])

    def test_translation(self, mocker):
        provider = random.choice(self.supported_providers)
        _provider_module = import_module(f"geranslator.provider.providers.{provider}")
        _provider_class = getattr(_provider_module, provider.capitalize())
        mocker.patch.object(_provider_class, "translate")

        Provider(provider).translate(["Hello"], "en", ["es", "fr"])
        _provider_class.translate.assert_called_once_with(["Hello"], "en", ["es", "fr"])
