#!/usr/bin/env python3

import unittest
from Scoring.Correctness.CorrectnessScore import CorrectnessScore


class MockCorrectnessScore:
    def __init__(self, stargazers_count, open_issues_count, forks_count):
        self.stargazers_count = stargazers_count
        self.open_issues_count = open_issues_count
        self.forks_count = forks_count


class CorrectnessScoreTests(unittest.TestCase):
    def test_worst_correctness(self):
        mock = MockCorrectnessScore(
            stargazers_count=0, open_issues_count=0, forks_count=0
        )
        sut = CorrectnessScore(mock)
        score = sut.score()
        self.assertEqual(score, 0)

    def test_best_correctness(self):
        mock = MockCorrectnessScore(
            stargazers_count=10000, open_issues_count=400, forks_count=10000
        )
        sut = CorrectnessScore(mock)
        score = sut.score()
        self.assertEqual(score, 1)


if __name__ == "__main__":
    unittest.main()
