from termspark import TermSpark

class ExtensionNotSupported(Exception):
    def __init__(self, extension: str):
        self.extension = extension

    def __str__(self) -> str:
        message = TermSpark().spark_left([f" {self.extension} ", 'white', 'red'], [f" file format not supported ", 'red'])

        return str(message)
