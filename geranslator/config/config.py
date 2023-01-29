import os
import yaml
import shutil

from typing import Optional
from ..exceptions.ConfigKeyNotFound import ConfigKeyNotFound

class Config:
    dir: str = os.path.dirname(os.path.realpath(__file__))
    config_file_name: str = '.geranslator-config.yaml'
    config_sample_file_name: str = '.geranslator-config.example'
    config_sample_relative_path: str = os.path.join('..', '..', config_sample_file_name)
    config_sample_path: str = os.path.join(dir, config_sample_relative_path)
    config_path: str = os.path.join(os.getcwd(), config_file_name)

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
        else:
            shutil.copy(self.config_sample_path, self.config_path)

            return self.get(key)
