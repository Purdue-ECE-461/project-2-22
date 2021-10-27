# NEW

from Scoring.ScoreBaseClass import ScoreBaseClass

class DependencyScore(ScoreBaseClass):
    def __init__(self, package):
        super().__init__(package)

    def score(self):
        return 99999