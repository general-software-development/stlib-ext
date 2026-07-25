from .color import color, Ansi
from .cursor import cursor, AnsiCursor
from .common import ControlSequenceIntroducer
from os_ext.details import plat_str
from os_ext import details

from types import SimpleNamespace

class ShellDetailsOSNamespace(SimpleNamespace):
    plat_str: str
    posix_compatible: bool

class ShellDetailsNamespace(SimpleNamespace):
    CSI: str
    ControlSequenceIntroducer: str
    os: ShellDetailsOSNamespace

class ShellNamespace(SimpleNamespace):
    color: Ansi
    cursor: AnsiCursor
    details: ShellDetailsNamespace

shell = ShellNamespace()
shell.color = color
shell.cursor = cursor

shell.details = ShellDetailsNamespace()
shell.details.CSI = ControlSequenceIntroducer
shell.details.ControlSequenceIntroducer = ControlSequenceIntroducer

shell.details.os = details

__all__ = (shell,)
