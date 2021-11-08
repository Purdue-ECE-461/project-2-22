# NEW

from Scoring.ScoreBaseClass import ScoreBaseClass
from Scoring.Dependency.Clone import clone_module

class DependencyScore(ScoreBaseClass):
    url = None
    name = None
    def __init__(self, package):
        self.url = package.html_url
        self.name = package.full_name
        super().__init__(package)

    def score(self):
        # print(self.package.full_name)
        # print(self.package.html_url)
        # print(self.package.url)
        # print(get_issues(self.package.full_name))
        score = clone_module(self.url, self.name)
        return score