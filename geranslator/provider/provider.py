import os

from typing import List
from importlib import import_module
from ..exceptions.ProviderNotFound import ProviderNotFound

class Provider:
    dir: str = os.path.dirname(os.path.realpath(__file__))
    provider: str

    def __init__(self, provider: str):
        self.__set_provider(provider.lower())

    def translate(self, lang_from_file: str, lang_to_files: List[str]):
        self.make_sure_provider_exists()

        _module = import_module(f"geranslator.provider.providers.{self.provider}")
        _class = getattr(_module, self.provider.capitalize())
        _class().translate(lang_from_file, lang_to_files)

    def __set_provider(self, provider: str):
        self.provider = provider

    def provider_exists(self) -> bool:
        return os.path.exists(os.path.join(self.dir, 'providers', f"{self.provider}.py"))

    def make_sure_provider_exists(self) -> bool:
        if not self.provider_exists():
            raise ProviderNotFound(self.provider)
        return True
