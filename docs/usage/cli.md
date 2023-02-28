# Usage / CLI
```bash
geranslator
```
### Supported options
| option | short | description |
|---|---|---|
| --provider        | -p | To specify provider.|
| --lang-dir        | -d | To specify translation files directory.|
| --extension       | -e | To specify translation files format.|
| --origin-lang     | -o | To specify the origin language.|
| --target-langs    | -t | To specify target languages.|

```bash
geranslator --provider=deepl --origin-lang=en --target-langs=es,pt
```
```bash
geranslator -p deepl -o en -t es,pt
```
> **Note**
> Keep in mind that default values are on `.geranslator-config.yaml` - [configuration](/configuration)
