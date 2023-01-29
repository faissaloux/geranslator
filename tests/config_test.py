import pytest

from geranslator.config.config import Config
from geranslator.exceptions.ConfigKeyNotFound import ConfigKeyNotFound

class TestConfig:

    def test_get_all_config_values(self):
        config = Config().get()

        assert isinstance(config, dict)
        assert len(config) == 5

    def test_get_specific_config_value(self):
        lang_dir = Config().get('lang_dir')

        assert isinstance(lang_dir, str)
        assert lang_dir == 'lang'

        to_langs = Config().get('to_langs')

        assert isinstance(to_langs, list)
        assert to_langs == ['fr', 'ar']

    def test_required_config_keys_exist(self):
        required_keys: dict = ['lang_dir', 'lang_files_ext', 'provider', 'origin_lang', 'to_langs']

        for key in required_keys:
            assert Config().get(key)

    def test_raise_exception_when_value_not_found(self):
        with pytest.raises(ConfigKeyNotFound):
            Config().get('not_exist')
