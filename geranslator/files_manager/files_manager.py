import os
import json
import yaml

from ..config.config import Config
from ..exceptions.FileNotFound import FileNotFound
from ..exceptions.ExtensionNotSupported import ExtensionNotSupported

class FilesManager:
    extension: str
    dir: str = Config().get('lang_dir')
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

    def set_dir(self, dir: str):
        self.dir = dir

        return self

    def insert(self):
        lang_dir = os.path.join(os.getcwd(), self.dir)
        lang_file = os.path.join(lang_dir, self.lang + '.' + self.extension)

        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)

        _method = getattr(self, f"insert_{self.ext_reference}")
        _method(lang_file)

    def get_keys(self) -> list:
        lang_dir = os.path.join(os.getcwd(), self.dir)
        lang_file = os.path.join(lang_dir, self.lang + '.' + self.extension)

        if os.path.exists(lang_file):
            _method = getattr(self, f"get_{self.ext_reference}_keys")
            return _method(lang_file)
        else:
            raise FileNotFound(lang_file)

    def __make_sure_extension_is_supported(self, extension) -> bool:
        for ext_reference, alias in self.ext_aliases.items():
            if extension in alias:
                self.ext_reference = ext_reference
                return True

        if not hasattr(self, f"insert_{extension}"):
            raise ExtensionNotSupported(extension)

        self.ext_reference = extension
        return True

    def insert_json(self, file: str):
        json.dump(self.data, open(file, "w"), indent=4, ensure_ascii = False)

    def get_json_keys(self, file: str) -> list:
        return list(json.load(open(file, "r")).keys())

    def insert_yaml(self, file: str):
        yaml.dump(self.data, open(file, "w"), allow_unicode = True)

    def get_yaml_keys(self, file: str) -> list:
        return list(yaml.load(open(file, "r"), Loader=yaml.Loader).keys())
