#!/usr/bin/env python3

# ScoreBaseClass.py
# Created by Charles Pisciotta
# September 21, 2021

from abc import ABC, abstractmethod


class ScoreBaseClass(ABC):
    @abstractmethod
    def __init__(self, package):
        self.package = package

    @abstractmethod
    def score(self):
        pass
