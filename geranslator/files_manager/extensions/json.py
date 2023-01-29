import json

from .abstractExtension import AbstractExtension

class Json(AbstractExtension):

    def insert(self, data: dict, file: str):
        json.dump(data, open(file, "w"), indent=4, ensure_ascii = False)

    def get_keys(self, file: str) -> list:
        return list(json.load(open(file, "r")).keys())
