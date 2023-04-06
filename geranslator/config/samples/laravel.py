import operator

from packaging import version

from geranslator.config.samples.sample import Sample


class Laravel(Sample):
    lang_dir: dict = {
        "<= 8": "lang",
        ">= 9": "resources/lang",
    }
    lang_files_ext: str = "json"

    def version(self, app_version: str):
        if app_version:
            operators: dict = {
                "<=": operator.le,
                ">=": operator.ge,
            }

            for version_condition, directory in self.lang_dir.items():
                condition, ver = version_condition.split(" ")
                operation = operators.get(condition)

                if operation and operation(
                    version.parse(app_version), version.parse(ver)
                ):
                    self.lang_dir = directory

        return self
