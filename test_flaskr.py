import os
import tempfile

import pytest

from main import app
import subprocess


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_post():
    with app.test_client() as c:
        rv = c.post('/package', json={
            "metadata": {
                "Name": "string",
                "Version": "1.2.3",
                "ID": "string"
            },
            "data": {
                "Content": "string",
                "URL": "string",
                "JSProgram": "string"
            }
        })
        json_data = rv.get_json()
        assert json_data["Name"] == "string"


def test_run():
    assert True


if __name__ == '__main__':
    print("fun")
