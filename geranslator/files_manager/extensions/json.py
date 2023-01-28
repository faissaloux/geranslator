import json

class Json:

    def insert(self, data: dict, file):
        json.dump(data, open(file, "w"), indent=4, ensure_ascii = False)

    def get_keys(self, file) -> list:
        return list(json.load(open(file, "r")).keys())
