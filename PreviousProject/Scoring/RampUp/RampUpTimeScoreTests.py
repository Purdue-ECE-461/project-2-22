#!/usr/bin/env python3

# RampUpTimeScoreTests.py
# Created by Jason Lei
# October 1, 2021
# Modified by Charles Pisciotta

import unittest
from Scoring.RampUp.RampUpTimeScore import RampUpTimeScore


# Define temporary package class to test this function on
class RampUpTestPackage:
    def __init__(self, forks, has_wiki, has_pages):
        self.forks_count = forks
        self.has_wiki = has_wiki
        self.has_pages = has_pages


class RampUpTimeScoreTests(unittest.TestCase):
    def test_0_correctness(self):
        mock = RampUpTestPackage(forks=0, has_wiki=False, has_pages=False)
        sut = RampUpTimeScore(mock)
        score = sut.score()
        self.assertEqual(score, 0)

    def test_0_25_correctness(self):
        mock = RampUpTestPackage(forks=50, has_wiki=False, has_pages=False)
        sut = RampUpTimeScore(mock)
        score = sut.score()
        self.assertEqual(score, 0.125)

    def test_0_5_correctness(self):
        mock = RampUpTestPackage(forks=500)
        sut = RampUpTimeScore(mock)
        score = sut.score()
        self.assertEqual(score, 0.5)

    def test_0_75_correctness(self):
        mock = RampUpTestPackage(forks=5000, has_wiki=True, has_pages=True)
        sut = RampUpTimeScore(mock)
        score = sut.score()
        self.assertEqual(score, 0.875)

    def test_1_correctness(self):
        mock = RampUpTestPackage(forks=10001, has_wiki=True, has_pages=True)
        sut = RampUpTimeScore(mock)
        score = sut.score()
        self.assertEqual(score, 1)


if __name__ == "__main__":
    unittest.main()
