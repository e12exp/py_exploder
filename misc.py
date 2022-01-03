import re

lmap=lambda *a:list(map(*a))

def inRange(x, min, max):
    if type(x)==type(""):
        x=int(x)
    if min<=x and x<=max:
        return x
    else:
        raise ValueError("%d is not in range [%d, %d]"%(x, min, max))

class ParseError(Exception):
    pass
