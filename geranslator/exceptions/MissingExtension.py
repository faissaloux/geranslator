from termspark import TermSpark

class MissingExtension(Exception):
    def __str__(self) -> str:
        message = TermSpark().spark_left([f" Extension is missing ", 'red'])

        return str(message)
