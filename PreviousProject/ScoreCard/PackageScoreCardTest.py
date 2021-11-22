#!/usr/bin/env python3

# PackageScoreCardTest.py
# Created by Jason Lei
# October 1, 2021

from ScoreCard.PackageScoreCard import PackageScoreCard


# PackageScoreCardTest tests the functionality of the PackageScoreCard class
def test():
    psc = PackageScoreCard(
        "fakeurl",
        total_score=0.5,
        bus_factor_score=0.5,
        correctness_score=0.5,
        license_score=0.5,
        ramp_up_score=0.5,
        responsiveness_score=0.5,
    )

    tests = [test1, test2, test3, test4, test5, test6]
    num_tests = len(tests)
    num_passed = 0

    # Perform tests
    for t in tests:
        num_passed += t(psc)

    # Return results
    return num_passed, num_tests


# Tests if url is present in toString()
def test1(psc):
    s = psc.toString()
    # Check url is present
    if str(psc.url) not in s:
        return 0
    return 1


# Tests if total score is present in toString()
def test2(psc):
    s = psc.toString()
    if str(psc.total_score) not in s:
        return 0
    return 1


# Tests if bus factor score is present in toString()
def test3(psc):
    s = psc.toString()
    if str(psc.bus_factor_score) not in s:
        return 0
    return 1


# Test if correctness score is present in toString()
def test4(psc):
    s = psc.toString()
    if str(psc.correctness_score) not in s:
        return 0
    return 1


# Test if license compatibility score is present in toString()
def test5(psc):
    s = psc.toString()
    if str(psc.license_compatibility_score) not in s:
        return 0
    return 1


# Test if ramp up score is present in toString()
def test6(psc):
    s = psc.toString()
    if str(psc.ramp_up_score) not in s:
        return 0
    return 1


# Test if responsiveness score is present in toString()
def test6(psc):
    s = psc.toString()
    if str(psc.responsiveness_score) not in s:
        return 0
    return 1


if __name__ == "__main__":
    test()
