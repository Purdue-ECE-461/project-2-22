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


def test_open_socket():
    result = subprocess.run(['./cloud_sql_proxy', '-instances=ece-461-project-2-22:us-east1:proj-2-database-mysql=tcp'
                                                  ':3306'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stderr)
    print(result.stdout)


if __name__ == '__main__':
    print("fun")
