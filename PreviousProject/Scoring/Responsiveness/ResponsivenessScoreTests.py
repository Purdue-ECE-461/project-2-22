#!/usr/bin/env python3

import unittest
from Scoring.Responsiveness.ResponsivenessScore import ResponsivenessScore


class MockResponsivenessPackage:
    def __init__(
        self,
        stargazers_count,
        open_issues_count,
        forks_count,
        watchers_count,
        network_count,
    ):
        self.stargazers_count = stargazers_count
        self.open_issues_count = open_issues_count
        self.forks_count = forks_count
        self.watchers_count = watchers_count
        self.network_count = network_count


class ResponsivenessScoreTests(unittest.TestCase):
    def test_0_responsiveness(self):
        mock = MockResponsivenessPackage(
            stargazers_count=0,
            open_issues_count=100000,
            forks_count=0,
            watchers_count=0,
            network_count=0,
        )
        sut = ResponsivenessScore(mock)
        score = sut.score()
        self.assertEqual(score, 0)

    def test_0_25_responsiveness(self):
        mock = MockResponsivenessPackage(
            stargazers_count=100,
            open_issues_count=300,
            forks_count=20,
            watchers_count=20,
            network_count=20,
        )
        sut = ResponsivenessScore(mock)
        score = sut.score()
        self.assertEqual(score, 0.25)

    def test_0_5_responsiveness(self):
        mock = MockResponsivenessPackage(
            stargazers_count=200,
            open_issues_count=200,
            forks_count=200,
            watchers_count=200,
            network_count=200,
        )
        sut = ResponsivenessScore(mock)
        score = sut.score()
        self.assertEqual(score, 0.5)

    def test_0_75_responsiveness(self):
        mock = MockResponsivenessPackage(
            stargazers_count=1001,
            open_issues_count=15,
            forks_count=1001,
            watchers_count=1001,
            network_count=1001,
        )
        sut = ResponsivenessScore(mock)
        score = sut.score()
        self.assertEqual(score, 0.75)

    def test_1_responsiveness(self):
        mock = MockResponsivenessPackage(
            stargazers_count=10001,
            open_issues_count=0,
            forks_count=10001,
            watchers_count=10001,
            network_count=10001,
        )
        sut = ResponsivenessScore(mock)
        score = sut.score()
        self.assertEqual(score, 1)


if __name__ == "__main__":
    unittest.main()
