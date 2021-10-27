#!/usr/bin/env python3

# CorrectnessScore.py
# Created by Charles Pisciotta
# September 15, 2021

from Scoring.ScoreBaseClass import ScoreBaseClass


# Correctness = Number of Stars * Number of Closed Issues * (Number of
# Open Issues + Number of Closed Issues)
class CorrectnessScore(ScoreBaseClass):
    def __init__(self, package):
        super().__init__(package)
        self.stargazers_count = package.stargazers_count
        self.open_issues_count = package.open_issues_count
        self.forks_count = package.forks_count

    def score(self):
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

        if self.open_issues_count > 500:
            open_issue_score = 0.5
        elif self.open_issues_count > 250:
            open_issue_score = 1
        elif self.open_issues_count > 100:
            open_issue_score = 0.5
        elif self.open_issues_count > 10:
            open_issue_score = 0.25
        else:
            open_issue_score = 0

        scores = [stargazer_score, open_issue_score, fork_score]
        return sum(scores) / len(scores)
