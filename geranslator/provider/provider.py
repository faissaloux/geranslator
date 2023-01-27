import os

from typing import List
from importlib import import_module
from ..exceptions.ProviderNotFound import ProviderNotFound

class Provider:
    dir: str = os.path.dirname(os.path.realpath(__file__))
    provider: str

    def __init__(self, provider: str):
        self.__set_provider(provider.lower())

    def translate(self, words: list, origin_lang: str, target_langs: List[str]) -> dict:
        self.make_sure_provider_exists()

        _module = import_module(f"geranslator.provider.providers.{self.provider}")
        _class = getattr(_module, self.provider.capitalize())

        return _class().translate(words, origin_lang, target_langs)

    def __set_provider(self, provider: str):
        self.provider = provider

    def provider_exists(self) -> bool:
        return os.path.exists(os.path.join(self.dir, 'providers', f"{self.provider}.py"))

    def make_sure_provider_exists(self) -> bool:
        if not self.provider_exists():
            raise ProviderNotFound(self.provider)
        return True
