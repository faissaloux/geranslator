import pytest
import random

from geranslator.provider.provider import Provider
from geranslator.exceptions.ProviderNotFound import ProviderNotFound

class TestProvider:
    supported_providers: list = [
        'google',
        'deepl',
    ]

    def test_set_provider(self):
        provider = Provider('google')

        assert provider.provider == 'google'

    def test_case_unsensitivity_provider(self):
        provider = Provider('GOOGLE')

        assert provider.provider == 'google'

    def test_supported_providers(self):
        for provider in self.supported_providers:
            assert Provider(provider).provider == provider

    def test_cant_translate_using_unexisted_provider(self):
        with pytest.raises(ProviderNotFound):
            Provider('unexisted').translate(['Hello'], 'en', ['ar', 'fr'])

    def test_translation(self):
        provider = random.choice(self.supported_providers)
        translation = Provider(provider).translate(['Hello'], 'en', ['es', 'fr'])

        assert translation == {'es': {'Hello': 'Hola'}, 'fr': {'Hello': 'Bonjour'}}
