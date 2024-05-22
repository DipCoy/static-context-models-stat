import math
from pprint import pprint
from typing import TextIO

from context_models.builder import ContextModelsBuilder
from custom_types import TextReader
from decapitalization.decapitalizer import Decapitalizer
from decapitalization.rules import (
    FirstTextLetterRule,
    UpperLetterAfterFullStopRule,
    UpperLetterAfterTwoUpperLettersRule,
)
from finbonacci_encoding import FibonacciEncoder

CHUNK_SIZE = 2 ** 9


def read_text(path: str) -> TextReader:
    with open(path, 'rt') as f:
        yield from read_in_chunks(f, chunk_size=CHUNK_SIZE)


def read_in_chunks(file_object: TextIO, *, chunk_size: int = 1024) -> TextReader:
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def main(text_file_path: str):
    rules = [
        FirstTextLetterRule(),
        UpperLetterAfterFullStopRule(),
        UpperLetterAfterTwoUpperLettersRule(),
    ]

    decapitalizer = Decapitalizer(rules)
    context_models_builder = ContextModelsBuilder(order=3)
    total_deviations = []
    for chunk in read_text(text_file_path):
        decapitalized_text, deviations = decapitalizer.decapitalize(chunk)
        total_deviations.extend(deviations)
        context_models_builder.process(decapitalized_text)

    context_models_builder.finalize()

    fib_encoder = FibonacciEncoder(max_number=CHUNK_SIZE + 1, zero=True)
    deviations_fib_encoded = fib_encoder.encode(total_deviations)

    print(f'Total Deviations number = {len(total_deviations)}')
    print(f'Fibonacci encoded Deviations Bytes length = {math.ceil(len(deviations_fib_encoded) / 8)}')
    three_order_context_models = context_models_builder.context_models

    total_context_models_size = sum(model.bytes_size for model in three_order_context_models)
    print(f'Total 3 Order Context Models number = {len(three_order_context_models)}')
    print(f'Total 3 Order Context Models Byte Size = {total_context_models_size} bytes')

    print(f'Deviations Fibonacci Encoded Bit Array: {deviations_fib_encoded}')
    input('3 order context models: Next? [Enter]')
    pprint(three_order_context_models)


if __name__ == '__main__':
    main('samples/CharlesDickens-OliverTwist.txt')
