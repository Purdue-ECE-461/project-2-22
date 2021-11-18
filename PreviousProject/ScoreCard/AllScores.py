#!/usr/bin/env python3

# AllScores.py
# Created by Jason Lei
# September 28, 2021

# Holds all the packages and their scores
class AllScores:
    def __init__(self, score_card_list):
        self.score_card_list = score_card_list

    def toString(self):
        # URL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE
        # RESPONSIVE_MAINTAINER_SCORE LICENSE_SCORE
        output_string = "URL NET_SCORE RAMP_UP_SCORE CORRECTNESS_SCORE BUS_FACTOR_SCORE RESPONSIVE_MAINTAINER_SCORE LICENSE_SCORE DEPENDENCY_SCORE\n"
        for score_card in self.score_card_list:
            output_string += score_card.toString() + "\n"

        return output_string
