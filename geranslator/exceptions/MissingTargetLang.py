from termspark import TermSpark

class MissingTargetLang(Exception):
    def __str__(self) -> str:
        message = TermSpark().spark_left([f" Target languages are missing ", 'red'])

        return str(message)
