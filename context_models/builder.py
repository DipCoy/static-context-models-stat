from collections import defaultdict

from utils import window
from .model import ContextModel


class ContextModelsBuilder:
    def __init__(self, *, order: int):
        self.__order = order
        self.__context_models = defaultdict(ContextModel)
        self.__last_context = ''
        self.__finalized = False

    def process(self, text: str) -> None:
        self.__check_not_finalized()
        processing_text = self.__last_context + text

        if len(processing_text) <= self.__order:
            self.__last_context = processing_text
            return

        for (*context_symbols, next_symbol) in window(processing_text, size=self.__order + 1):
            string = ''.join(context_symbols)
            self.__process_context(string, next_symbol=next_symbol)

        self.__last_context = string[1:] + next_symbol

    def finalize(self) -> None:
        self.__check_not_finalized()
        self.__process_context(self.__last_context, next_symbol=None)
        self.__finalized = True

    @property
    def context_models(self) -> list[ContextModel]:
        return list(self.__context_models.values())

    def __check_not_finalized(self) -> None:
        if self.__finalized:
            raise ValueError('Already finalized')

    def __process_context(self, context: str, *, next_symbol: str | None) -> None:
        if len(context) < self.__order:
            self.__last_context = context
            return

        context_model = self.__context_models[context]
        context_model.string = context
        context_model.count += 1
        self.__last_context = context[1:]

        if next_symbol is not None:
            context_model.add_next_symbol(next_symbol)
            self.__last_context = context[1:] + next_symbol
