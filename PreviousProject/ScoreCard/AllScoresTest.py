#!/usr/bin/env python3

# AllScoresTest.py
# Created by Jason Lei
# October 1, 2021

from PreviousProject.ScoreCard.AllScores import AllScores
from PreviousProject.ScoreCard.PackageScoreCard import PackageScoreCard


# Tests the AllScores data structure
def test():
    testScores1 = PackageScoreCard(
        "fakeurl",
        total_score=0.5,
        bus_factor_score=0.5,
        correctness_score=0.5,
        license_score=0.5,
        ramp_up_score=0.5,
        responsiveness_score=0.5,
    )

    testScores2 = PackageScoreCard(
        url="fakeurl",
        total_score=0.5,
        bus_factor_score=0.5,
        correctness_score=0.5,
        license_score=0.5,
        ramp_up_score=0.5,
        responsiveness_score=0.5,
    )

    allScores = AllScores([testScores1, testScores2])

    tests = [test1]
    num_tests = len(tests)
    num_passed = 0

    # Perform tests
    for t in tests:
        num_passed += t(allScores, [testScores1, testScores2])

    # Return results
    return num_passed, num_tests


# Tests the toString functionality of the AllScores class
def test1(allScores, testScores):
    str1 = allScores.toString()
    for s in testScores:
        if s.toString() not in str1:
            return 0
    return 1


if __name__ == "__main__":
    test()
