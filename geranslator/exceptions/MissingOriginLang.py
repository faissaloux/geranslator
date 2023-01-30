from termspark import TermSpark

class MissingOriginLang(Exception):
    def __str__(self) -> str:
        message = TermSpark().spark_left([f" Origin language is missing ", 'red'])

        return str(message)
