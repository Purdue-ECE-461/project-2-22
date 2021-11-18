#!/usr/bin/env python3

import json
import unittest
from Scoring.LicenseCompatibility.LicenseCompatibilityScore import (
    LicenseCompatibilityScore,
)


class LicenseTestPackage:
    def __init__(self, license):
        self.license = license


class LicenseCompatibilityTests(unittest.TestCase):
    def test_no_license_1(self):
        mock = LicenseTestPackage(None)
        sut = LicenseCompatibilityScore(mock)
        score = sut.score()
        self.assertEqual(score, 0)

    def test_license_1(self):
        mock_json = '{"license": {"name": "MIT License"}}'
        mock_dict = json.loads(mock_json)
        mock = LicenseTestPackage(**mock_dict)
        sut = LicenseCompatibilityScore(mock)
        score = sut.score()
        self.assertEqual(score, 1)

    def test_license_2(self):
        mock_json = '{"license":{"name":"GPLv3"}}'
        mock_dict = json.loads(mock_json)
        mock = LicenseTestPackage(**mock_dict)
        sut = LicenseCompatibilityScore(mock)
        score = sut.score()
        self.assertEqual(score, 1)


if __name__ == "__main__":
    unittest.main()
