import termspark.termspark

class UnsupportedLanguage(Exception):
    def __init__(self, language: str):
        self.language = language

    def __str__(self):
        message = termspark.TermSpark().spark_left([f" {self.language} ", 'white', 'red'], [f" language not supported ", 'red'])
        return str(message)
