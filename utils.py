from itertools import islice
from typing import TypeVar, Tuple, Iterable

T = TypeVar('T')


def window(seq: Iterable[T], *, size: int) -> Tuple[T, ...]:
    """
    Returns a sliding window (of width n) over data from the iterable
    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
    """
    it = iter(seq)
    result = tuple(islice(it, size))
    if len(result) == size:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result
