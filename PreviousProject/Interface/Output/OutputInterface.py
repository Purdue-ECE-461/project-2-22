#!/usr/bin/env python3

# OutputInterface.py
# Created by Jason Lei
# September 23, 2021

from PreviousProject.Interface.Interface import Interface
from PreviousProject.DEBUG import DEBUG

# The OutputInterface organizes the system output based on what mode is
# being run and the information provided to it.


class OutputInterface(Interface):
    def __init__(self, mode="idle"):
        super().__init__(mode)

    # Print results based on what mode the interface is in
    def showResults(self, results):
        if self.mode == Interface.INSTALL_MODE:
            print(self.formatInstallResults(results))
        elif self.mode == Interface.TEST_MODE:
            results_string = self.formatTestResults(results)
            print(results_string)
        elif self.mode == Interface.RANK_MODE:
            results_string = self.formatRankResults(results)
            print(results_string)

            if DEBUG:
                with open("output_1.txt", "w") as outputFile:
                    outputFile.write(results_string)
        else:
            print("Output Interface is in Idle mode")

    # Formats the number of dependencies installed
    @staticmethod
    def formatInstallResults(installResults):
        return """{} dependencies installed...""".format(installResults)

    # Formats the results of the test cases and the line coverage achieved.
    @staticmethod
    def formatTestResults(testResults):
        passed = testResults[0]
        total = testResults[1]
        coverage = passed / total * 100

        formatted_string = "Total: {}\nPassed: {}\n{}/{} test cases passed. {}% line coverage achieved."
        return formatted_string.format(total, passed, passed, total, coverage)

    # Formats the results in string format. The rank results data structure
    # MUST have a toString() method.
    @staticmethod
    def formatRankResults(rankResults):
        return rankResults
