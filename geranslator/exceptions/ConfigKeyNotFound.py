import termspark.termspark

class ConfigKeyNotFound(Exception):
    def __init__(self, key: str):
        self.key = key

    def __str__(self):
        message = termspark.TermSpark().spark_left([f" {self.key} ", 'white', 'red'], [f" not found in config file ", 'red'])
        return str(message)
