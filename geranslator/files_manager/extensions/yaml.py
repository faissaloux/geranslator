import yaml

from .abstractExtension import AbstractExtension

class Yaml(AbstractExtension):

    def insert(self, data: dict, file: str):
        yaml.dump(data, open(file, "w"), allow_unicode = True)

    def get_keys(self, file: str) -> list:
        return list(yaml.load(open(file, "r"), Loader=yaml.Loader).keys())
