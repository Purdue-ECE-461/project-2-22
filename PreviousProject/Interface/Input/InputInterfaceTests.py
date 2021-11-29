#!/usr/bin/env python3

# InputInterfaceTest.py
# Created by Jason Lei
# October 1, 2021


import unittest
from Interface.Input.InputInterface import InputInterface, INSTALL_COMMAND, TEST_COMMAND
from Interface.Interface import Interface


class InputInterfaceTests(unittest.TestCase):

    input_interface: InputInterface

    def setUp(self) -> None:
        self.input_interface = InputInterface()

    def tearDown(self) -> None:
        self.input_interface = None

    def test_install(self):
        mode, urls = self.input_interface.determineMode(INSTALL_COMMAND)
        self.assertEqual(mode, INSTALL_COMMAND)
        self.assertEqual(self.input_interface.mode, Interface.INSTALL_MODE)

    def test_test(self):
        mode, urls = self.input_interface.determineMode(TEST_COMMAND)
        self.assertEqual(mode, TEST_COMMAND)
        self.assertEqual(self.input_interface.mode, Interface.TEST_MODE)

    def test_rank(self):
        mode, urls = self.input_interface.determineMode(
            "./Testing/sample_url_file.txt")
        self.assertEqual(mode, "rank")
        self.assertEqual(self.input_interface.mode, Interface.RANK_MODE)
        self.assertIsNotNone(urls)


if __name__ == "__main__":
    unittest.main()
