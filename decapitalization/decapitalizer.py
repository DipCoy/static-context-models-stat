from custom_types import Symbol, DeviationsPositions, DecapitalizedText
from .rules import DecapitalizationRule, RuleCheckResult


class Decapitalizer:
    def __init__(self, rules: list[DecapitalizationRule]):
        self.__rules = rules

    def decapitalize(self, text: str) -> (DecapitalizedText, DeviationsPositions):
        deviations_positions = []

        for position, symbol in enumerate(text):
            symbol: Symbol
            check_results = set(rule.eat(symbol) for rule in self.__rules)

            if (
                    RuleCheckResult.MATCHED_DEVIATION in check_results or
                    symbol.isupper() and all(result is RuleCheckResult.NOT_MATCHED for result in check_results)
            ):
                deviations_positions.append(position + 1)

        return text.lower(), deviations_positions

