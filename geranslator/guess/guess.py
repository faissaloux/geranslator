import re
import subprocess


class Guess:
    applications_cmd: dict = {
        "laravel": "php artisan --version",
        "symfony": "php bin/console --version",
    }

    def application(self) -> list:
        application_version = None

        for application, cmd in self.applications_cmd.items():
            response = subprocess.getstatusoutput(cmd)

            if response[0] == 0:
                version_found = re.search(r"(\d+\.)+\d+", response[1])

                if version_found:
                    application_version = version_found.group(0)

                return [application, application_version]

        return ["sample", application_version]
