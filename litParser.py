"""Parse an object connecting an internal line (dt%d, bp%d) to inputs and outputs"""

from word_dict import *


def parse(d, wd):
    """parse a litaral assignment, set addr val"""
    if d["name"]!="set":
        raise ParseError
    addr=d["addr"]
    val= d["val"]
    wd.setVal(addr, val)
if __name__=="__main__":
    print(parseInput("tbus1.3"))
    print(parseInternal("bp12"))
    print(parseOutput("mbs12"))
