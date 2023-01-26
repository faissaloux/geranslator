from termspark import TermSpark

class ConfigKeyNotFound(Exception):
    def __init__(self, key: str):
        self.key = key

    def __str__(self) -> str:
        message = TermSpark().spark_left([f" {self.key} ", 'white', 'red'], [f" not found in config file ", 'red'])

        return str(message)
