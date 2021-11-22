#!/usr/bin/env python3

# Interface.py
# Created by Jason Lei
# September 23, 2021

from abc import ABC, abstractmethod


# The interface class is an abstract class upon which user interfaces are
# built.
class Interface(ABC):
    IDLE_MODE = 0
    INSTALL_MODE = 1
    TEST_MODE = 2
    RANK_MODE = 3

    @abstractmethod
    def __init__(self, mode="idle"):
        # The interface changes based on what mode is provided.
        # It can be in install, test, rank, or idle mode.
        # If it is in idle mode, something went wrong.
        if mode == "install":
            self.mode = Interface.INSTALL_MODE
        elif mode == "test":
            self.mode = Interface.TEST_MODE
        elif mode == "rank":
            self.mode = Interface.RANK_MODE
        else:
            self.mode = Interface.IDLE_MODE
        pass
