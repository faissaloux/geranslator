from termspark import TermSpark

class MissingProvider(Exception):
    def __str__(self) -> str:
        message = TermSpark().spark_left([f" Provider is missing ", 'red'])

        return str(message)
