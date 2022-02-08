#!/usr/bin/python3

from copy import deepcopy
from word_dict import *
import matrixParser as mp
import litParser as lp
import pulserParser as pp

parsers=[mp, lp, pp]

import yaml


    

def parse(inp, wd=None):
    #print("parsing: %s"%inp)
    if not wd:
        wd=WordDict()
    else:
        wd=deepcopy(wd)
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

if __name__=="__main__":
    settings_in, mappings=yaml.load_all(open("exploder.yaml"))
    default=parse(settings_in["default"])
    settings=dmap(lambda inp: (inp[0], parse(inp[1], wd=default)),
                 settings_in.items())
    
    #    mp.parse({"name":"bp0", "in":["lemo0", "lemo2"], "out":["mbs12", "lemo3"]},  wd)
    for name, wd in settings.items():
        print("==%s=="%name)
        #wd.dump()
    settings["master"].verify(1)

