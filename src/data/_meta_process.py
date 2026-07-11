from typing import Any

class ProcessMeta(type):
    __output_classes__: tuple[type, ...]

    def __new__(mcls, name: str, bases: tuple[type, ...], namespace: dict[str, Any], *, output_classes: tuple[type, ...], **kwargs: Any) -> type:
        oldnew = namespace["__new__"]

        def __new__(cls: type, *args: Any, **kwargs: Any) -> Any:
            value = oldnew(cls, *args, **kwargs)
        
            for t in output_classes:
                if isinstance(value, t):
                    break
            else:
                raise TypeError(f"Data processor `{name}` returned a value of type {type(value)} -- not one of {output_classes}")
            
            return value
        
        def __init__(self: Any, *_: Any, **__: Any) -> None:
            raise RuntimeError(f"Attempted to initialise instance of {type(self)} (data processor). Invalid operation.")
        
        namespace["__init__"] = __init__
        namespace["__new__"] = __new__
        namespace["__output_classes__"] = output_classes

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        return cls
    
    def __instancecheck__(cls: "ProcessMeta", instance: object) -> bool:
        for t in cls.__output_classes__:
            if isinstance(instance, t):
                return True
                
        return False
