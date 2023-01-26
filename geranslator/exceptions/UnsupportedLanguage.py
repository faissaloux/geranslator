from termspark import TermSpark

class UnsupportedLanguage(Exception):
    def __init__(self, language: str):
        self.language = language

    def __str__(self) -> str:
        message = TermSpark().spark_left([f" {self.language} ", 'white', 'red'], [f" language not supported ", 'red'])

        return str(message)
