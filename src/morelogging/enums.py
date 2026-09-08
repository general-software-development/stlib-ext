from enum import Enum
from dataclasses import dataclass
from moretyping.data.mutable_enum import MutableEnum

@dataclass
class LogLevelItem:
    name: str
    level: int

    def __hash__(self):
        return hash((self.name, self.level))

class LogLevel(MutableEnum[LogLevelItem]):
    DEBUG = None
    INFO = None
    WARNING = None
    ERROR = None
    CRITICAL = None

def add_log_level(name: str, level: int) -> None:
    LogLevel.add(name, LogLevelItem(level = level, name = name))

add_log_level("DEBUG", 0)
add_log_level("INFO", 20)
add_log_level("WARNING", 40)
add_log_level("ERROR", 60)
add_log_level("CRITICAL", 80)
