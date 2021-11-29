import pytest


def multiplication():
    return 5*5


def test_multiply():
    assert multiplication() == 25


if __name__ == "__main__":
    test_multiply()
