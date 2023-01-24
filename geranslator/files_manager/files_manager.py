import os
import json

from ..config.config import Config
from ..exceptions.FileNotFound import FileNotFound

class FilesManager:
    extension: str = Config().get('lang_files_ext')
    data: dict
    lang: str

    def set_extension(self, extension: str):
        self.extension = extension

        return self

    def set_data(self, data: dict):
        self.data = data

        return self

    def set_lang(self, lang: str):
        self.lang = lang

        return self

    def insert(self):
        lang_dir = os.path.join(os.getcwd(), Config().get('lang_dir'))
        lang_file = os.path.join(lang_dir, self.lang + '.' + self.extension)

        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)

        _method = getattr(self, f"insert_{self.extension}")
        _method(lang_file)

    def get_keys(self) -> list:
        lang_dir = os.path.join(os.getcwd(), Config().get('lang_dir'))
        lang_file = os.path.join(lang_dir, self.lang + '.' + self.extension)

        if os.path.exists(lang_file):
            _method = getattr(self, f"get_{self.extension}_keys")
            return _method(lang_file)
        else:
            raise FileNotFound(lang_file)

    def insert_json(self, file: str):
        json.dump(self.data, open(file, "w"), indent=4, ensure_ascii = False)

    def get_json_keys(self, file: str) -> list:
        return list(json.load(open(file, "r")).keys())
