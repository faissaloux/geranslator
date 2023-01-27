import pytest

from geranslator.provider.provider import Provider
from geranslator.exceptions.ProviderNotFound import ProviderNotFound

class TestProvider:

    def test_set_provider(self):
        provider = Provider('google')

        assert provider.provider == 'google'

    def test_case_unsensitivity_provider(self):
        provider = Provider('GOOGLE')

        assert provider.provider == 'google'

    def test_make_sure_existing_provider_exist(self):
        provider = Provider('google')

        assert provider.make_sure_provider_exists() == True

    def test_make_sure_unexisting_provider_unexist(self):
        with pytest.raises(ProviderNotFound):
            Provider('unexisted').make_sure_provider_exists()

    def test_cant_translate_using_unexisted_provider(self):
        with pytest.raises(ProviderNotFound):
            Provider('unexisted').translate(['Hello'], 'en', ['ar', 'fr'])

    def test_translation(self):
        translation = Provider('google').translate(['Hello'], 'en', ['es', 'pt'])

        assert translation == {'es': {'Hello': 'Hola'}, 'pt': {'Hello': 'Olá'}}
