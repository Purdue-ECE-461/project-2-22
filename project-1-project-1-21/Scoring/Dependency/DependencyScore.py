# NEW

from Scoring.ScoreBaseClass import ScoreBaseClass
from Scoring.Dependency.Clone import clone_module

class DependencyScore(ScoreBaseClass):
    package = None
    def __init__(self, package):
        self.package = package
        super().__init__(package)

    def score(self):
        # print(self.package.full_name)
        # print(self.package.html_url)
        # print(self.package.url)
        # print(get_issues(self.package.full_name))
        score = clone_module(self.package.html_url, self.package.full_name)
        return score