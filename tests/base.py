import warnings

def register_test(func):
    func.__test__ = True
    return func

class _TestSuite:
    __targets__ = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__test__ = True

        targets = getattr(cls, "__targets__", tuple())

        if targets is None or len(targets) == 0:
            warnings.warn(f"{cls.__name__} is defined as a test suite, but has no test targets. Please define __targets__", RuntimeWarning)

        for func in targets:
            func.__test__ = True

        for name, func in cls.__dict__.items():
            if name.startswith("test") and func not in targets:
                warnings.warn(f"{cls.__name__}.{name} appears to be a test suite, but is not registered as one in __targets__", RuntimeWarning)

if __name__ == "__main__":
    import os

    os.system("pytest -v")
