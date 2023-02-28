# Usage / IDE
This will use the configuration as default - [configuration](/configuration)
```python
    from geranslator import Geranslator

    Geranslator().translate()
```

You can customize it using the following methods. 😃
```python
    from geranslator import Geranslator

    geranslator = Geranslator()
    geranslator.set_provider('google')
    geranslator.set_lang_dir('translation')
    geranslator.set_origin_lang('en')
    geranslator.set_target_lang(['ar', 'fr'])
    geranslator.set_lang_files_extension('json')
    geranslator.translate()
```
You can chain them too 😮
```python
    from geranslator import Geranslator

    Geranslator().set_provider('google').set_lang_dir('translation').set_origin_lang('en').set_target_lang(['ar', 'fr']).set_lang_files_extension('json').translate()
```
