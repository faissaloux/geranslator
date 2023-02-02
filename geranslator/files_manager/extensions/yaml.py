import yaml

from .abstractExtension import AbstractExtension

class Yaml(AbstractExtension):

    def insert(self, data: dict, file: str):
        yaml.dump(data, open(file, "w"), allow_unicode = True)

    def get(self, file: str) -> dict:
        return yaml.load(open(file, "r"), Loader=yaml.Loader)
