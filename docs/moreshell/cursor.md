# `shell.cursor` &mdash; Move the cursor using ANSI codes

## cursor

```py
cursor: AnsiCursor = ...
```

## Outline

```py
class AnsiCursor:
    def UP(self, n=1):
        ...
    
    def DOWN(self, n=1):
        ...
    
    def FORWARD(self, n=1):
        ...
    
    def BACK(self, n=1):
        ...
    
    def POS(self, x=1, y=1):
        ...
```
