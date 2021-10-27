#!/usr/bin/env python3

# PackageScoreCard.py
# Created by Jason Lei
# September 28, 2021

# Holds all the scores for a single package
class PackageScoreCard:
    def __init__(
        self,
        url,
        total_score=0,
        bus_factor_score=0,
        correctness_score=0,
        license_score=0,
        ramp_up_score=0,
        responsiveness_score=0,
    ):
        self.url = url
        self.total_score = total_score
        self.bus_factor_score = bus_factor_score
        self.correctness_score = correctness_score
        self.license_compatibility_score = license_score
        self.ramp_up_score = ramp_up_score
        self.responsiveness_score = responsiveness_score

    def toString(self):
        # URL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE
        # RESPONSIVE_MAINTAINER_SCORE LICENSE_SCORE
        score_string = (
            str(self.url).rstrip()
            + " "
            + str(round(self.total_score, 1))
            + " "
            + str(round(self.ramp_up_score, 1))
            + " "
            + str(round(self.correctness_score, 1))
            + " "
            + str(round(self.bus_factor_score, 1))
            + " "
            + str(round(self.responsiveness_score, 1))
            + " "
            + str(round(self.license_compatibility_score, 1))
        )
        return score_string
