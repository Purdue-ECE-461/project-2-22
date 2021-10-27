#!/usr/bin/env python3

# LicenseCompatibilityScore.py
# Created by Charles Pisciotta
# September 15, 2021
# Edited by Jason Lei
# October 3, 2021

from Scoring.ScoreBaseClass import ScoreBaseClass


class LicenseCompatibilityScore(ScoreBaseClass):
    def __init__(self, package):
        super().__init__(package)

    def score(self):
        if self.package.license is None:
            return 0

        # Pull license information from package
        license_info = self.package.license

        if "name" not in license_info:
            return 0

        license_name = license_info["name"]

        # If package has no license at all, give a score of 0.
        if license_name is None:
            print("Out!")
            return 0

        # List of licenses supported, i.e. GNU LGPLv2.1 or higher
        supported_licenses = [
            "GNU Lesser General Public License",
            "Lesser General Public License",
            "LGPL",
            "General Public License",
            "GPL",
            "MIT License",
            "GNU Lesser General Public License v2.1",
            "lgpl-2.1",
            "GPLv3",
        ]

        # Check if this package has any of the supported licenses. If yes, give
        # license score of 1.
        if license_name in supported_licenses:
            return 1
        else:
            return 0
