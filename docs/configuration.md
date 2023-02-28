# Configuration
> .geranslator-config.yaml

It's gonna be created for you. 😌

Just need to know it's there whenever you want to update default values.

```yaml
geranslator:
  lang_dir: lang
  lang_files_ext: json
  provider: google
  origin_lang: en
  target_langs: [fr, ar]
```

- lang_dir: Where your translation files live.
- lang_files_ext: Your translation files extension.
- provider: Provider you want to translate your file.
- origin_lang: The origin language you already have.
- target_langs: Languages you want your file to get translated to.

> supported extensions: json, yaml, yml, po

> supported providers: google, deepl
