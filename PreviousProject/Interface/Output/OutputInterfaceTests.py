#!/usr/bin/env python3

import unittest
from Interface.Interface import Interface
from Interface.Output.OutputInterface import OutputInterface
from random import randrange
from ScoreCard.PackageScoreCard import PackageScoreCard


class OutputInterfaceTests(unittest.TestCase):
    def test_install(self):
        output_interface = OutputInterface()
        output_interface.mode = "install"
        random_num = randrange(100)
        output = output_interface.formatInstallResults(random_num)
        self.assertEqual(
            "{} dependencies installed...".format(random_num),
            output)
        self.assertEqual(output_interface.mode, Interface.INSTALL_MODE)

    def test_test(self):
        output_interface = OutputInterface()
        output_interface.mode = "test"
        random_total = randrange(100)
        random_succeed = randrange(random_total)

        output = output_interface.formatTestResults(
            [random_succeed, random_total])
        self.assertEqual(
            output,
            "Total: {}\nPassed: {}\n{}/{} test cases passed. {}% line coverage achieved.".format(
                random_total,
                random_succeed,
                random_succeed,
                random_total,
                100),
        )
        self.assertEqual(output_interface.mode, Interface.TEST_MODE)

    def test_rank(self):
        output_interface.mode = "rank"
        score_card = PackageScoreCard(
            url="fakeurl",
            total_score=0.5,
            bus_factor_score=0.5,
            correctness_score=0.5,
            license_score=0.5,
            ramp_up_score=0.5,
            responsiveness_score=0.5,
        )

        output_interface = OutputInterface()
        output = output_interface.formatRankResults(score_card)
        if score_card.toString() in output:
            s = 1
        else:
            s = 0
        self.assertEqual(s, 1)
        self.assertEqual(output_interface.mode, Interface.RANK_MODE)


if __name__ == "__main__":
    unittest.main()
