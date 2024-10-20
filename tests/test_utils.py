import os

import pytest

from seiright.utils.utils import get_env_var


class TestGetEnvVar:
    def test_env_var(self, mocker):
        mocker.patch.dict(os.environ, {"SECRET_KEY": "some-key"})
        assert get_env_var("SECRET_KEY") == "some-key"

    def test_raise_error(self):
        with pytest.raises(KeyError):
            get_env_var("SECRET_KEY")
