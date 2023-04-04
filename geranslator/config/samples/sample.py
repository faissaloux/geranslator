from typing import Union


class Sample:
    lang_dir: Union[str, dict] = "lang"
    lang_files_ext: str = "json"
    provider: str = "google"
    origin_lang: str = "en"
    target_langs: list = ["fr", "ar"]

    def make(self) -> dict:
        config = {}

        for attribute in self.__get_attributes():
            config[attribute] = getattr(self, attribute)

        return config

    def __get_attributes(self) -> dict:
        attributes: dict = {}

        for classs in self.__class__.__mro__:
            try:
                attributes.update(**classs.__annotations__)
            except AttributeError:
                pass

        return attributes

    def version(self, app_version: str):
        return self
