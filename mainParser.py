#!/usr/bin/python3

from copy import deepcopy
from word_dict import *
import requireParser as rp
import matrixParser as mp
import litParser as lp
import pulserParser as pp
parsers=[rp, mp, lp, pp]

import yaml

settings_in=None

def parse(inp, wd=None):
    #print("parsing: %s"%inp)
    if wd==None:
        wd=WordDict()

    for l in inp:
        for p in parsers+[None]:
            if p==None:
                raise Exception("Could not parse obj {%s}"%l)
            try:
                p.parse(l, wd)
                break
            except ParseError:
                pass # go on
            except Exception as e:
                raise Exception("Parser %s failed to parse %s"%(p.__name__, l)) from e
    return wd

def load(fname="exploder.yaml"):
    global settings_in
    settings_in, mappings=yaml.load_all(open(fname))
    settings=dmap(lambda inp: (inp[0], parse(inp[1])),
                         settings_in.items())
    return settings, mappings

if __name__=="__main__":
    pass
