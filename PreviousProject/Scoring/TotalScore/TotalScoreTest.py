#!/usr/bin/env python3

# TotalScoreTest.py
# Created by Jason Lei
# October 1, 2021
import Scoring.TotalScore.TotalScore


# TotalScoreTest tests the functionality of the TotalScore class
def test():
    ts = TotalScore.TotalScore([1, 0, 0.5, 0.25, 0.75])

    tests = [test1]
    num_tests = len(tests)
    num_passed = 0

    # Perform tests
    for t in tests:
        num_passed += t(ts)

    # Return results
    return num_passed, num_tests


# Tests the functionality of TotalScore's score() function
def test1(ts):
    score = ts.score()
    if score != 0.5:
        return 0
    return 1


if __name__ == "__main__":
    test()
