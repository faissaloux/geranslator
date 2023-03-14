from typing import List

import typer

from ..config.config import Config
from ..geranslator import Geranslator


class CommandLine:
    app = typer.Typer()

    def main(self):
        self.app()

    @app.command()
    def translate(
        self=None,  # type: ignore
        provider: str = typer.Option(Config().get("provider"), "--provider", "-p"),
        lang_dir: str = typer.Option(Config().get("lang_dir"), "--lang-dir", "-d"),
        extension: str = typer.Option(
            Config().get("lang_files_ext"), "--extension", "-e"
        ),
        origin_lang: str = typer.Option(
            Config().get("origin_lang"), "--origin-lang", "-o"
        ),
        target_langs: List[str] = typer.Option(
            Config().get("target_langs"), "--target-langs", "-t"
        ),
    ):
        arguments: dict = locals()

        for arg, val in arguments.items():
            if val != None:
                if isinstance(val, list):
                    if val[0].startswith("="):
                        arguments[arg] = [val[0][1:]]
                else:
                    if val.startswith("="):
                        arguments[arg] = val[1:]

        if "," in arguments["target_langs"][0]:
            arguments["target_langs"] = arguments["target_langs"][0].split(",")

        geranslator = Geranslator()
        geranslator.set_provider(arguments["provider"])
        geranslator.set_lang_dir(arguments["lang_dir"])
        geranslator.set_lang_files_extension(arguments["extension"])
        geranslator.set_origin_lang(arguments["origin_lang"])
        geranslator.set_target_lang(arguments["target_langs"])
        geranslator.translate()
