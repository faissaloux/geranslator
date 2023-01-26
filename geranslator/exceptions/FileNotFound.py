from termspark import TermSpark

class FileNotFound(Exception):
    def __init__(self, file: str):
        self.file = file

    def __str__(self) -> str:
        message = TermSpark().spark_left([f" {self.file} ", 'white', 'red'], [f" file not found ", 'red'])

        return str(message)
