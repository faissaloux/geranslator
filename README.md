![Logo](https://raw.githubusercontent.com/faissaloux/geranslator/main/.github/art/logo.png)

[![Test Python package](https://github.com/faissaloux/geranslator/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/faissaloux/geranslator/actions/workflows/tests.yml) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/faissaloux/geranslator/main.svg)](https://results.pre-commit.ci/latest/github/faissaloux/geranslator/main) ![PyPI](https://img.shields.io/pypi/v/geranslator) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/geranslator) ![PyPI - Status](https://img.shields.io/pypi/status/geranslator)

# Installation
```bash
    pip install geranslator
```
# Configuration
> geranslator/config.yml
```yml
geranslator:
  lang_dir: lang
  lang_files_ext: json
  provider: google
  origin_lang: en
  to_langs:
  - en
  - fr
  - ar

```
- lang_dir: Where your translation files live.
- lang_files_ext: Your translation files extension.
- provider: Provider you want to translate your file.
- origin_lang: The origin language you already have.
- to_langs: Languages you want your file to get translated to.

> supported extensions: json

> supported providers: google
# Usage
This will use the configuration as default
```python
    from geranslator import Geranslator

    Geranslator().translate()
```

You can customize it using the following methods. 😃
```python
    from geranslator import Geranslator

    geranslator = Geranslator()
    geranslator.set_lang_dir('translation')
    geranslator.set_origin_lang('en')
    geranslator.set_target_lang(['ar', 'fr'])
    geranslator.set_lang_files_extension('json')
    geranslator.translate()
```
You can chain them too 😮
```python
    from geranslator import Geranslator

    Geranslator().set_lang_dir('translation').set_origin_lang('en').set_target_lang(['ar', 'fr']).set_lang_files_extension('json').translate()
```
