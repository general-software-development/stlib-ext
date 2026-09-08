from moretyping.meta import Unknown

class MutableEnumMeta(type):
    def __iter__(cls):
        return iter(cls._members.values())

    def __len__(cls):
        return len(cls._members)

    def __instancecheck__(cls, instance):
        return instance in cls._members.values()

class MutableEnum[T = Unknown](metaclass=MutableEnumMeta):
    def __init__(self, object: T) -> None:
        self.value = object

    def __init_subclass__(cls):
        cls._members = {}

    @classmethod
    def add(cls, name, value):
        if hasattr(cls, name) and getattr(cls, name) is not None:
            raise ValueError(f"{cls.__name__} already has an attribute named {name!r}")

        member = cls(value)
        cls._members[name] = member
        setattr(cls, name, member)
        return member

    def __getattribute__(self, name: str) -> T:
        return super().__getattribute__(name)
