#!/usr/bin/python3

import matrixParser as mp

class WordDict(dict):
    """A dictionary object meant to store 32 bit words as a 
       addr->val map"""
    def setBit(self, addr, bit):
        """Set a specific bit at a specific address"""
        self.setdefault(addr, 0)
        self[addr]|=1<<bit
    def setVal(self, addr, val):
        self[addr]=val
    

def canParse(name, function):
    try:
        f(l["name"])
        return True
    except ParseError:
        return False
    
def parse(inp):
    res=WordDict()    
    for l in inp:
        pass

if __name__=="__main__":
    wd=WordDict()
    mp.parse({"name":"bp0", "out":["mbs12"]},  wd)
    print(wd)
             
