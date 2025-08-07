from collections.abc import Callable

from hypothesis.strategies import SearchStrategy

def given[T1, T2](
    arg1: SearchStrategy[T1],
    arg2: SearchStrategy[T2],
) -> Callable[[Callable[[T1, T2], None]], Callable[[], None]]: ...
