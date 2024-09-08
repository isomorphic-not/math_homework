import typing
from dataclasses import dataclass

import numpy


@dataclass
class Operation:
    fn: typing.Callable[[int, int], int]
    symbol: str


operations_map = {
    numpy.add.__name__: Operation(fn=numpy.add, symbol="+"),
    numpy.subtract.__name__: Operation(fn=numpy.subtract, symbol="-"),
    numpy.multiply.__name__: Operation(fn=numpy.multiply, symbol="*"),
    numpy.divide.__name__: Operation(fn=numpy.divide, symbol="/"),
}
