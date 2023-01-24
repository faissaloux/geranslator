import termspark.termspark

class ProviderNotFound(Exception):
    def __init__(self, provider: str):
        self.provider = provider

    def __str__(self):
        message = termspark.TermSpark().spark_left([f" {self.provider} ", 'white', 'red'], [f" provider not found ", 'red'])
        return str(message)
