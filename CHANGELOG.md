## [Unreleased](https://github.com/faissaloux/geranslator/compare/v1.3.0...main)

## [v1.3.0](https://github.com/faissaloux/geranslator/compare/v1.2.4...v1.3.0) - 2023-10-22
### ADDED
- Py3.12 support ([#92](https://github.com/faissaloux/geranslator/pull/92))

## [v1.2.4](https://github.com/faissaloux/geranslator/compare/v1.2.3...v1.2.4) - 2023-10-08
### FIXED
- Fix unexisted language detection ([#88](https://github.com/faissaloux/geranslator/pull/88))

## [v1.2.3](https://github.com/faissaloux/geranslator/compare/v1.2.2...v1.2.3) - 2023-07-29
### FIXED
- Fix Chrome Driver after v115 url not found ([#81](https://github.com/faissaloux/geranslator/pull/81))

## [v1.2.2](https://github.com/faissaloux/geranslator/compare/v1.2.1...v1.2.2) - 2023-06-02
### FIXED
- Fix google provider ([#75](https://github.com/faissaloux/geranslator/pull/75))

## [v1.2.1](https://github.com/faissaloux/geranslator/compare/v1.2.0...v1.2.1) - 2023-04-09
### FIXED
- Fix update prefixed files ([#69](https://github.com/faissaloux/geranslator/pull/69))

## [v1.2.0](https://github.com/faissaloux/geranslator/compare/v1.1.1...v1.2.0) - 2023-04-08
### ADDED
- Config file depending on application ([#65](https://github.com/faissaloux/geranslator/pull/65))
### FIXED
- Prevent translations override ([#67](https://github.com/faissaloux/geranslator/pull/67))

## [v1.1.1](https://github.com/faissaloux/geranslator/compare/v1.1.0...v1.1.1) - 2023-04-05
### FIXED
- Update deepl changed elements ([#64](https://github.com/faissaloux/geranslator/pull/64))

### ADDED
- Support lang files names with prefix ([#62](https://github.com/faissaloux/geranslator/pull/62))

## [v1.1.0](https://github.com/faissaloux/geranslator/compare/v1.0.5...v1.1.0) - 2023-03-22
### ADDED
- Support lang files names with prefix ([#62](https://github.com/faissaloux/geranslator/pull/62))

## [v1.0.5](https://github.com/faissaloux/geranslator/compare/v1.0.4...v1.0.5) - 2023-03-15
### FIXED
- Fix multiple target langs CLI parameter ([#59](https://github.com/faissaloux/geranslator/pull/59))
### INTERNAL
- Add `update_docs_changelog` Makefile target ([#60](https://github.com/faissaloux/geranslator/pull/60))

## [v1.0.4](https://github.com/faissaloux/geranslator/compare/v1.0.3...v1.0.4) - 2023-03-15
### FIXED
- Fix cmd arguments with `=` sign ([#58](https://github.com/faissaloux/geranslator/pull/58))

## [v1.0.3](https://github.com/faissaloux/geranslator/compare/v1.0.2...v1.0.3) - 2023-03-14
### FIXED
- Fix `dictionary` file not included on build ([#57](https://github.com/faissaloux/geranslator/pull/57))

## [v1.0.2](https://github.com/faissaloux/geranslator/compare/v1.0.1...v1.0.2) - 2023-03-14
### FIXED
- Fix `extensions` directory not included on build ([#56](https://github.com/faissaloux/geranslator/pull/56))
- Fix `AttributeError: 'staticmethod' object has no attribute '__name__'` ([#55](https://github.com/faissaloux/geranslator/pull/55))

## [v1.0.1](https://github.com/faissaloux/geranslator/compare/v1.0.0...v1.0.1) - 2023-03-14
### FIXED
- Fix Config Example File not included on build ([#54](https://github.com/faissaloux/geranslator/pull/54))

## [v1.0.0](https://github.com/faissaloux/geranslator/compare/v0.3.0...v1.0.0) - 2023-02-28
### ADDED
- Translation progress ([#46](https://github.com/faissaloux/geranslator/pull/46))
- Skip `hidden` words from each file format ([#41](https://github.com/faissaloux/geranslator/pull/41))

## [v0.3.0](https://github.com/faissaloux/geranslator/compare/v0.2.0...v0.3.0) - 2023-02-05
### ADDED
- CLI ([#38](https://github.com/faissaloux/geranslator/pull/38))
- Deepl support ([#28](https://github.com/faissaloux/geranslator/pull/28))
- Po support ([#24](https://github.com/faissaloux/geranslator/pull/24))
### CHANGED
- Translate value instead of key ([#35](https://github.com/faissaloux/geranslator/pull/35))
- Case unsensitive extensions ([#21](https://github.com/faissaloux/geranslator/pull/21))
## FIXED
- Fix deepl translation bug ([#37](https://github.com/faissaloux/geranslator/pull/37))

## [v0.2.0](https://github.com/faissaloux/geranslator/compare/v0.1.0...v0.2.0) - 2023-01-27
### ADDED
- Yaml support ([#20](https://github.com/faissaloux/geranslator/pull/20))
- Choosing provider ([#15](https://github.com/faissaloux/geranslator/pull/15))
- Handle network exception ([#12](https://github.com/faissaloux/geranslator/pull/12))
### REMOVED
- Remove Translator ([#11](https://github.com/faissaloux/geranslator/pull/11))
### FIXED
- Fix setting files extension ([#19](https://github.com/faissaloux/geranslator/pull/19))
- Fix reading files from set directory ([#17](https://github.com/faissaloux/geranslator/pull/17))
- Fix setting lang dir ([#16](https://github.com/faissaloux/geranslator/pull/16))

## v0.1.0 - 2023-01-25
### ADDED
- Geranslator ([#7](https://github.com/faissaloux/geranslator/pull/7))
- Provider ([#6](https://github.com/faissaloux/geranslator/pull/6))
- Files manager ([#5](https://github.com/faissaloux/geranslator/pull/5))
- Google provider ([#4](https://github.com/faissaloux/geranslator/pull/4))
- Languages dictionary ([#3](https://github.com/faissaloux/geranslator/pull/3))
- Translator ([#2](https://github.com/faissaloux/geranslator/pull/2))
