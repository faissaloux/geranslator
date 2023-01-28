import yaml

class Yaml:

    def insert(self, data: dict, file):
        yaml.dump(data, open(file, "w"), allow_unicode = True)

    def get_keys(self, file) -> list:
        return list(yaml.load(open(file, "r"), Loader=yaml.Loader).keys())
