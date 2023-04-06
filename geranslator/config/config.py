import os
from importlib import import_module
from typing import Optional

import yaml

from geranslator.files_manager.extensions.yaml import Yaml
from geranslator.guess.guess import Guess

from ..exceptions.ConfigKeyNotFound import ConfigKeyNotFound


class Config:
    dir: str = os.path.dirname(os.path.realpath(__file__))
    config_file_name: str = ".geranslator-config.yaml"
    config_path: str = os.path.join(os.getcwd(), config_file_name)

    def get(self, key: Optional[str] = None):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as config_file:
                config = yaml.load(config_file, Loader=yaml.Loader)
                if key:
                    if key in config["geranslator"]:
                        return config["geranslator"][key]
                    else:
                        raise ConfigKeyNotFound(key)
                else:
                    return config["geranslator"]
        else:
            self.__create_config_file()

            return self.get(key)

    def __create_config_file(self):
        application = Guess().application()

        _module = import_module(f"geranslator.config.samples.{application[0].lower()}")
        _class = getattr(_module, application[0].capitalize())

        config = _class().version(application[1]).make()

        Yaml().insert({"geranslator": config}, self.config_path)
