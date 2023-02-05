import typer

from typing import List
from ..geranslator import Geranslator
from ..config.config import Config

class CommandLine:
    app = typer.Typer()

    def main(self):
        self.app()

    @app.command()
    @staticmethod
    def translate(
        provider: str = typer.Option(Config().get('provider'), '--provider', '-p'),
        lang_dir: str = typer.Option(Config().get('lang_dir'), '--lang-dir', '-d'),
        extension: str = typer.Option(Config().get('lang_files_ext'), '--extension', '-e'),
        origin_lang: str = typer.Option(Config().get('origin_lang'), '--origin-lang', '-o'),
        target_langs: List[str] = typer.Option(Config().get('target_langs'), '--target-langs', '-t')
    ):
        if ',' in target_langs[0]:
            target_langs = target_langs[0].split(',')

        geranslator = Geranslator()
        geranslator.set_provider(provider)
        geranslator.set_lang_dir(lang_dir)
        geranslator.set_lang_files_extension(extension)
        geranslator.set_origin_lang(origin_lang)
        geranslator.set_target_lang(target_langs)
        geranslator.translate()
