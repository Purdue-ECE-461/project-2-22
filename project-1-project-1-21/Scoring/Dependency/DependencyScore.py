# NEW

from Scoring.ScoreBaseClass import ScoreBaseClass
from Scoring.Dependency.Clone import clone_module

class DependencyScore(ScoreBaseClass):
    def __init__(self, package):
        super().__init__(package)
        self.url = package.html_url
        self.name = package.full_name

    def score(self):
        # print(self.package.full_name)
        # print(self.package.html_url)
        # print(self.package.url)
        # print(get_issues(self.package.full_name))
        score = clone_module(self.url, self.name)
        return score