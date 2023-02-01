import os

from importlib import import_module
from ..config.config import Config
from ..exceptions.FileNotFound import FileNotFound
from ..exceptions.ExtensionNotSupported import ExtensionNotSupported

class FilesManager:
    extension: str
    dir: str = os.path.dirname(os.path.realpath(__file__))
    langs_dir: str = Config().get('lang_dir')
    data: dict
    lang: str
    ext_aliases: dict = {
        "yaml": ["yml"],
    }

    def __init__(self):
        self.set_extension(Config().get('lang_files_ext'))

    def set_extension(self, extension: str):
        self.__make_sure_extension_is_supported(extension)
        self.extension = extension

        return self

    def set_data(self, data: dict):
        self.data = data

        return self

    def set_lang(self, lang: str):
        self.lang = lang

        return self

    def set_langs_dir(self, dir: str):
        self.langs_dir = dir

        return self

    def insert(self):
        lang_dir = os.path.join(os.getcwd(), self.langs_dir)
        lang_file = os.path.join(lang_dir, self.lang + '.' + self.extension)

        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)

        self.__ext_class().insert(self.data, lang_file)

    def get(self) -> list:
        lang_dir = os.path.join(os.getcwd(), self.langs_dir)
        lang_file = os.path.join(lang_dir, self.lang + '.' + self.extension)

        if os.path.exists(lang_file):
            return self.__ext_class().get(lang_file)
        else:
            raise FileNotFound(lang_file)

    def __make_sure_extension_is_supported(self, extension) -> bool:
        self.ext_reference = extension
        for ext_reference, alias in self.ext_aliases.items():
            if extension in alias:
                self.ext_reference = ext_reference

        if not self.__extensions_is_supported():
            raise ExtensionNotSupported(extension)

        __ext_module = import_module(f"geranslator.files_manager.extensions.{self.ext_reference}")
        self.__ext_class = getattr(__ext_module, self.ext_reference.capitalize())

        return True

    def __extensions_is_supported(self) -> bool:
        return os.path.exists(os.path.join(self.dir, 'extensions', f"{self.ext_reference}.py"))
