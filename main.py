from moretyping import vis
from moretyping import data
from morefunctools import cache
from morefunctools import experimental

@cache.fifo_cache(1)
def test(a, **kwargs):
    return 2 + a

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

if __name__ == "__main__":
    main()

# This is a test file. This is not included in the library.
