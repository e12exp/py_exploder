
from word_dict import *
import re
def parse(d, wd):
    """Parse a line configuring a pulser input"""
    m=re.match("pulser([0-3])", d["name"])
    if not m:
        raise ParseError
    pulser=int(m.group(1))
    addr=0x83+pulser
    if "freq" in d:
        if d["freq"]>0:
            freq=float(d["freq"])
            val=int(100e6/freq-1)
        else:
            val=0
    elif "val" in d:
        val=int(d["val"])
    else:
        raise Exception("Must specify freq or val with name='pulser...' in %s"%d)
    wd.setVal(addr, val)
