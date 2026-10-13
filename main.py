from moretyping import vis
from moretyping import data
from morefunctools import cache
from morefunctools import experimental
from moremath import Equation, SquareRoot, Root

@cache.fifo_cache(1)
def test(a, **kwargs):
    return 2 + a

#@cache.fifo_cache(True)
#def add(a, b):
#    return a + b

@experimental
def main():
    values = [1, 2, 3, 4, 5]
    values.append(6)
    link = vis.VisLink(values)
    jsonv = vis.ViewJSON(values)
    print(link)
    print(jsonv)
    morevalues = {"test": 2, "test.more": "2.8"}
    print(vis.ViewJSON(morevalues))

    print(data.Number(8), data.Number("4"), data.Number("4.2"))

    print(test(1))
    print(test(1, test = "test"))
    print(test(2))
    print(test(1))

    eq = Equation(2) * 2 + 3 - 1
    print(eq)
    print(eq.resolve())
    print(SquareRoot(-4))
    print(SquareRoot(-3))
    print(Root(-8, 3))
    print(2 * SquareRoot(3) + 5 - 1 + 2)
    print((2 * SquareRoot(3) + 5 - 1 + 2).resolve())

    add(1, 2)
    print(add.cache_info())  

if __name__ == "__main__":
    main()

# This is a test file. This is not included in the library.

from src import morelogging

#morelogging.__internal_test()
