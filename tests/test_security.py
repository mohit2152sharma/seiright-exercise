import os

import pytest

from seiright.app.security import (
    access_token_expire_time,
    algorithm,
    authenticate_user,
    secret_key,
)


@pytest.fixture
def db():
    return {"test": {"username": "test", "display_name": "Test"}}


class TestSecurity:
    def test_security(self, mocker):
        mocker.patch.dict(os.environ, {"SECRET_KEY": "some-key"})
        assert secret_key() == "some-key"

    def test_algorithm(self, mocker):
        mocker.patch.dict(os.environ, {"ALGORITHM": "some-algo"})
        assert algorithm() == "some-algo"

    def test_access_time(self):
        assert access_token_expire_time() == 30

    def test_authenticate_non_existing_user(self, db):
        assert authenticate_user(db, "new_user", "test") is False
