import functools

from utils import window


def _fibonacci_sequence(lte: int):
    if lte < 1:
        return

    current_number = 1
    next_number = 2

    yield current_number

    if lte == 1:
        return

    yield next_number

    while True:
        t = next_number
        next_number = next_number + current_number
        current_number = t
        if next_number > lte:
            break
        yield next_number


@functools.cache
def fibonacci_sequence(lte: int) -> list[int]:
    return [f for f in _fibonacci_sequence(lte)]


@functools.cache
def fibonacci_sequence_set(lte: int) -> set[int]:
    return set(fibonacci_sequence(lte))


_BIN_STR = str


class FibonacciEncoder:
    def __init__(self, *, max_number: int, zero: bool = False):
        self.__fibonacci_sequence = fibonacci_sequence(max_number)
        self.__fibonacci_set = set(self.__fibonacci_sequence)
        self.__fibonacci_index = {number: index + 1 for index, number in enumerate(self.__fibonacci_sequence)}
        self.__zero = zero

    def encode(self, numbers: list[int]) -> _BIN_STR:
        encoded_numbers = [self.__encode(number) for number in numbers]
        return '1'.join(encoded_numbers)

    def decode(self, s: _BIN_STR) -> list[int]:
        split_string = self.__split_encoded(s)
        zero_delta = 1 if self.__zero else 0
        return [self.__from_fibonacci_representation(encoded_number) - zero_delta for encoded_number in split_string]

    def __split_encoded(self, s: _BIN_STR) -> list[_BIN_STR]:
        if not s:
            return []

        if len(s) == 1:
            return [s]

        buffer = []
        words = []
        flushed = False
        for prev_symbol, current_symbol in window(s, size=2):
            if flushed:
                flushed = False
                continue
            buffer.append(prev_symbol)

            if prev_symbol == current_symbol == '1':
                words.append(''.join(buffer))
                flushed = True
                buffer = []

        if not (prev_symbol == current_symbol == '1'):
            buffer.append(current_symbol)
            words.append(''.join(buffer))

        return words

    def __encode(self, number: int) -> _BIN_STR:
        if self.__zero:
            number = number + 1

        fibonacci_indices = self.__represent_as_fibonacci_sum_index(number)

        encoded = []
        for i in range(1, fibonacci_indices[0] + 1):
            encoded.append('1' if i in fibonacci_indices else '0')

        return ''.join(encoded)

    def __represent_as_fibonacci_sum_index(self, number: int) -> list[int]:
        fibonacci_sum = self.__represent_as_fibonacci_sum(number)
        return [self.__fibonacci_index[fib] for fib in fibonacci_sum]

    def __represent_as_fibonacci_sum(self, number: int) -> list[int]:
        fibonacci_numbers = fibonacci_sequence(number)
        if not fibonacci_numbers:
            return []

        if number in fibonacci_sequence_set(number):
            return [number]

        max_fibonacci_number = fibonacci_numbers[-1]
        return [max_fibonacci_number, *self.__represent_as_fibonacci_sum(number - max_fibonacci_number)]

    def __from_fibonacci_representation(self, s: _BIN_STR) -> int:
        fibonacci_indices = [i + 1 for i, symbol in enumerate(s) if symbol == '1']

        result = 0
        for index in fibonacci_indices:
            result += self.__fibonacci_sequence[index - 1]

        return result
