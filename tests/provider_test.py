import pytest

from importlib import import_module
from unittest.mock import patch
from geranslator.provider.provider import Provider
from geranslator.exceptions.ProviderNotFound import ProviderNotFound

class TestProvider:

    def test_set_provider(self):
        provider = Provider()
        provider.set_provider('google')

        assert provider.provider == 'google'

    def test_make_sure_existing_provider_exist(self):
        provider = Provider()
        provider.set_provider('google')

        provider.make_sure_provider_exists()

    def test_make_sure_unexisting_provider_unexist(self):
        provider = Provider()
        provider.set_provider('unexisted')

        with pytest.raises(ProviderNotFound):
            provider.make_sure_provider_exists()
