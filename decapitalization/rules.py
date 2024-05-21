from enum import Enum, auto
from typing import Protocol

from custom_types import Symbol


class RuleCheckResult(Enum):
    NOT_MATCHED = auto()
    MATCHED_DEVIATION = auto()
    MATCHED_OK = auto()


class DecapitalizationRule(Protocol):
    def eat(self, symbol: Symbol) -> RuleCheckResult:
        ...


class FirstTextLetterRule:
    def __init__(self):
        self.__last_symbol = None

    def eat(self, symbol: Symbol) -> RuleCheckResult:
        if self.__last_symbol is not None:
            return RuleCheckResult.NOT_MATCHED

        self.__last_symbol = symbol
        if self.__last_symbol.isupper():
            return RuleCheckResult.MATCHED_OK

        return RuleCheckResult.MATCHED_DEVIATION


class UpperLetterAfterFullStopRule:
    def __init__(self):
        self.__found_full_stop = False

    def eat(self, symbol: Symbol) -> RuleCheckResult:
        if symbol.isspace():
            return RuleCheckResult.NOT_MATCHED

        if symbol == '.':
            self.__found_full_stop = True
            return RuleCheckResult.NOT_MATCHED

        if symbol.isalpha() and self.__found_full_stop:
            self.__found_full_stop = False

            if symbol.isupper():
                return RuleCheckResult.MATCHED_OK

            return RuleCheckResult.MATCHED_DEVIATION

        if self.__found_full_stop:
            self.__found_full_stop = False

        return RuleCheckResult.NOT_MATCHED


class UpperLetterAfterTwoUpperLettersRule:
    def __init__(self):
        self.__upper_count = 0

    def eat(self, symbol: Symbol) -> RuleCheckResult:
        if not symbol.isalpha():
            self.__upper_count = 0
            return RuleCheckResult.NOT_MATCHED

        if symbol.islower():
            if self.__upper_count == 2:
                self.__upper_count = 0
                return RuleCheckResult.MATCHED_DEVIATION

            self.__upper_count = 0
            return RuleCheckResult.NOT_MATCHED

        if self.__upper_count in (0, 1):
            self.__upper_count += 1
            return RuleCheckResult.NOT_MATCHED

        if self.__upper_count == 2:
            return RuleCheckResult.MATCHED_OK

