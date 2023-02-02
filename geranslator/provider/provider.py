import os

from typing import List
from importlib import import_module
from ..exceptions.ProviderNotFound import ProviderNotFound

class Provider:
    dir: str = os.path.dirname(os.path.realpath(__file__))
    provider: str

    def __init__(self, provider: str):
        self.__set_provider(provider.lower())

    def translate(self, text: dict, origin_lang: str, target_langs: List[str]) -> dict:
        _module = import_module(f"geranslator.provider.providers.{self.provider}")
        _class = getattr(_module, self.provider.capitalize())

        return _class().translate(text, origin_lang, target_langs)

    def __set_provider(self, provider: str):
        self.__make_sure_provider_exists(provider)

        self.provider = provider

    def provider_exists(self, provider: str) -> bool:
        return os.path.exists(os.path.join(self.dir, 'providers', f"{provider}.py"))

    def __make_sure_provider_exists(self, provider: str) -> bool:
        if not self.provider_exists(provider):
            raise ProviderNotFound(provider)
        return True
