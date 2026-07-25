# Copyright Jonathan Hartley 2013. BSD 3-Clause license

ControlSequenceIntroducer = '\033['

def code_to_chars(code):
    return ControlSequenceIntroducer + str(code) + 'm'

class AnsiCodes:
    def __init__(self):
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))
