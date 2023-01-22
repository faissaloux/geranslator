import termspark.termspark

class OriginLangFileNotFound(Exception):
    def __init__(self, origin_lang_file: str):
        self.origin_lang_file = origin_lang_file

    def __str__(self):
        message = termspark.TermSpark().spark_left([f" {self.origin_lang_file} ", 'white', 'red'], [f" not found ", 'red'])
        return str(message)
