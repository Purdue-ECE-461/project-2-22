#!/usr/bin/env python3

import unittest
from Scoring.BusFactor.BusFactorScore import BusFactorScore


class MockBusFactorPackage:
    def __init__(self, stargazers_count, watchers_count, forks_count):
        self.stargazers_count = stargazers_count
        self.watchers_count = watchers_count
        self.forks_count = forks_count


class BusFactorScoreTests(unittest.TestCase):
    def test_worst_bus_factor(self):
        mock = MockBusFactorPackage(
            stargazers_count=0,
            watchers_count=0,
            forks_count=0)
        sut = BusFactorScore(mock)
        score = sut.score()
        self.assertEqual(score, 0)

    def test_best_bus_factor(self):
        mock = MockBusFactorPackage(
            stargazers_count=10000, watchers_count=10000, forks_count=10000
        )
        sut = BusFactorScore(mock)
        score = sut.score()
        self.assertEqual(score, 1)


if __name__ == "__main__":
    unittest.main()
