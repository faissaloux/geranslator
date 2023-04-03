class Sample:
    lang_dir: str = "lang"
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
