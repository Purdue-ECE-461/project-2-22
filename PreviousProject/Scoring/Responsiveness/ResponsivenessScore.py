#!/usr/bin/env python3

# ResponsivenessScore.py
# Created by Charles Pisciotta
# September 15, 2021

from PreviousProject.Scoring.ScoreBaseClass import ScoreBaseClass


class ResponsivenessScore(ScoreBaseClass):
    def __init__(self, package):
        super().__init__(package)
        self.stargazers_count = package.stargazers_count
        self.open_issues_count = package.open_issues_count
        self.forks_count = package.forks_count
        self.watchers_count = package.watchers_count
        self.network_count = package.network_count

    def score(self):
        if self.stargazers_count > 10000:
            stargazer_score = 1
        elif self.stargazers_count > 1000:
            stargazer_score = 0.75
        elif self.stargazers_count > 100:
            stargazer_score = 0.5
        elif self.stargazers_count > 10:
            stargazer_score = 0.25
        else:
            stargazer_score = 0

        if self.watchers_count > 10000:
            watcher_score = 1
        elif self.watchers_count > 1000:
            watcher_score = 0.75
        elif self.watchers_count > 100:
            watcher_score = 0.5
        elif self.watchers_count > 10:
            watcher_score = 0.25
        else:
            watcher_score = 0

        if self.forks_count > 10000:
            fork_score = 1
        elif self.forks_count > 1000:
            fork_score = 0.75
        elif self.forks_count > 100:
            fork_score = 0.5
        elif self.forks_count > 10:
            fork_score = 0.25
        else:
            fork_score = 0

        if self.open_issues_count > 500:
            open_issue_score = 0
        elif self.open_issues_count > 250:
            open_issue_score = 0.25
        elif self.open_issues_count > 100:
            open_issue_score = 0.5
        elif self.open_issues_count > 10:
            open_issue_score = 0.75
        else:
            open_issue_score = 1

        scores = [stargazer_score, watcher_score, fork_score, open_issue_score]
        return sum(scores) / len(scores)
