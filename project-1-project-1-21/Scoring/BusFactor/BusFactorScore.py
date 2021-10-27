#!/usr/bin/env python3

# BusFactorScore.py
# Created by Charles Pisciotta
# September 15, 2021

from Scoring.ScoreBaseClass import ScoreBaseClass


class BusFactorScore(ScoreBaseClass):
    def __init__(self, package):
        super().__init__(package)
        self.stargazers_count = package.stargazers_count
        self.watchers_count = package.watchers_count
        self.forks_count = package.forks_count

    def score(self):
        # Determine a sub-score based on number of stargazers
        if self.stargazers_count > 1000:
            stargazer_score = 1
        elif self.stargazers_count > 500:
            stargazer_score = 0.75
        elif self.stargazers_count > 100:
            stargazer_score = 0.5
        elif self.stargazers_count > 10:
            stargazer_score = 0.25
        else:
            stargazer_score = 0

        # Determine a sub-score based on number of watchers
        if self.watchers_count > 1000:
            watcher_score = 1
        elif self.watchers_count > 500:
            watcher_score = 0.75
        elif self.watchers_count > 100:
            watcher_score = 0.5
        elif self.watchers_count > 10:
            watcher_score = 0.25
        else:
            watcher_score = 0

        # Determine a sub-score for number of forks
        if self.forks_count > 1000:
            fork_score = 1
        elif self.forks_count > 500:
            fork_score = 0.75
        elif self.forks_count > 100:
            fork_score = 0.5
        elif self.forks_count > 10:
            fork_score = 0.25
        else:
            fork_score = 0

        # Final score is an average of the 3
        scores = [stargazer_score, watcher_score, fork_score]
        return sum(scores) / len(scores)
