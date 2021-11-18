import unittest
from DependencyScore import DependencyScore

class DependencyTestPackage:
    def __init__(self, url, name):
        self.url = url
        self.name = name

class DependencyTimeScoreTests(unittest.TestCase):
    def test(self):
        mock = DependencyTestPackage(url="https://github.com/nullivex/nodist", name="nullivex/nodist")
        sut = DependencyScore(mock)
        score = sut.score()
        assert(score > 0)


# Not finished