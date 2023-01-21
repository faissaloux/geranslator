import os
import yaml
from typing import Optional
from ..exceptions.ConfigKeyNotFound import ConfigKeyNotFound

class Config:
    dir: str = os.path.dirname(os.path.realpath(__file__))
    config_relative_path: str = os.path.join('..', 'config.yml')
    config_path: str = os.path.join(dir, config_relative_path)

    def get(self, key: Optional[str] = None):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as config_file:
                config = yaml.load(config_file, Loader=yaml.Loader)
                if key:
                    if key in config['geranslator']:
                        return config['geranslator'][key]
                    else:
                        raise ConfigKeyNotFound(key)
                else:
                    return config['geranslator']
