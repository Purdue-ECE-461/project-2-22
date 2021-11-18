#!/usr/bin/env python3

# TotalScore.py
# Created by Charles Pisciotta
# September 15, 2021
# Edited by Jason Lei
# October 1, 2021


# TotalScore is a scorer that determines the average score of a package
# based on a given list of scores.
class TotalScore:
    def __init__(self, scores):
        self.scores = scores

    def score(self):
        # Tracks the number of scores as well as the unweighted total of them
        num_scores = len(self.scores)
        total = sum(self.scores)

        # Total score rating is the average of all the scores provided
        return total / num_scores
