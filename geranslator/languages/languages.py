import os
import yaml

class Languages:
    dir: str = os.path.dirname(os.path.realpath(__file__))
    dictionary_path: str = os.path.join(dir, 'dictionary.yml')

    def get(self, abbr: str) -> str:
        with open(self.dictionary_path, "r") as config_file:
            dictionary = yaml.load(config_file, Loader=yaml.Loader)

            return dictionary[abbr] if abbr in dictionary else abbr
