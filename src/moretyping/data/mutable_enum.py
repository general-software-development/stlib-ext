class MutableEnumMeta(type):
    def __iter__(cls):
        return iter(cls._members.values())

    def __len__(cls):
        return len(cls._members)

    def __instancecheck__(cls, instance):
        return instance in cls._members.values()

class MutableEnum(metaclass=MutableEnumMeta):
    def __init_subclass__(cls):
        cls._members = {}

    @classmethod
    def add(cls, name, value):
        if hasattr(cls, name):
            raise ValueError(f"{cls.__name__} already has an attribute named {name!r}")

        cls._members[name] = value
        setattr(cls, name, value)
        return value
