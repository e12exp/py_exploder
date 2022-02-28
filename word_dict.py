#!/usr/bin/python3

import re
from subprocess import run, check_output

lmap=lambda *a:list(map(*a))
dmap=lambda *a:dict(map(*a))

def inRange(x, min, max):
    if type(x)==type(""):
        x=int(x)
    if min<=x and x<=max:
        return x
    else:
        raise ValueError("%d is not in range [%d, %d]"%(x, min, max))


def region_name(addr):
    """Return the section topic for a config address"""
    if addr<0 or addr>=0x2000:
        return "invalid"
    if addr<63: # input matrix
        if addr<16:
            return "in->dt"
        elif addr<32:
            return "in->bp"
        else:
            return "in->special"
    elif addr<0x80: # output matrix
        addr-=0x40
        if addr==0:
            return "(int)->NC"
        elif addr<16:
            return "(int)->MBS"
        elif addr<24:
            return "(int)->TBus"
        elif addr<31:
            return "(int)->lemo"
        elif addr<40:
            return "(int)->LVDS"
        elif addr<64:
            return "(int)->scaler"
    elif addr<0x1000:
        return "???"
    elif addr<0x1200: # extended input matrix
        addr-=0x1000
        addr/=4
        return "ext:%s"%region_name(addr)
    elif addr<0x1280:
        addr-=0x1200
        addr/=4
        return "ext:%s"%region_name(addr+0x40)
    
        
class WordDict(dict):
    """A dictionary object meant to store 32 bit words as a 
       addr->val map"""
    def __init__(self):
        """plus some more cruft:"""
        self.labels={} # scaler channel -> name
        self.lines=[] # list of line names

    def setBit(self, addr, bit):
        """Set a specific bit at a specific address"""
        self.setdefault(addr, 0)
        self[addr]|=1<<bit
    def setVal(self, addr, val):
        self[addr]=val
    def dump(self, quiet=True):
        for a, v in sorted(self.items(), key=lambda a:a[0]):
            if (not quiet or v!=0):
                print("0x%08x: 0x%08x"%(a, v))
        for x in self.labels.items():
            print("Scaler %d: %s"%x)

    def _read_block(self, exp_id, start, num):
        """Read a block from an exploder, overwriting settings"""
        res=check_output(["/usr/bin/exploder", "read", "%s"%exp_id, "0x%x"%start, "0x%x"%num]).decode("utf-8")
        for l in res.split("\n"):
            if l=="":
                continue
            addr, val=map(lambda i: int(i, 0), l.split(":"))
            self[addr]=val

    def update_scalers(self, exp_id):
        self._read_block(exp_id, 0x100,   0x100)

    def scaler(self, i, latched=True, clock=False):
        return self[0x100+4*i+2*latched+clock]

    def dump_scalers(self, exp_id):
        self.update_scalers(exp_id)
        for i, n in self.labels.items():
            print("%30s: %10d"%(n, self.scaler(i)))
    
    def read(self, exp_id):
        self._read_block(exp_id, 0,       0x100)
        self._read_block(exp_id, 0x1000, 0x1000)

    def _write_block(self, exp_id, start, num):
        """Writes a block to an exploder id"""
        input=""
        for addr in range(start, start+num):
            input+="0x%x\n"%self.get(addr, 0)
        proc=run(["/usr/bin/exploder","write", "%s"%exp_id, "0x%x"%start, "0x%x"%num, "-"],
                 check=True, input=input, text=True)
        
    def write(self, exp_id, check=True):
        self._write_block(exp_id, 0,       0x100)
        self._write_block(exp_id, 0x1000, 0x1000)

    def verify(self, exp_id, verbose=True):
        wd=WordDict()
        wd.read(exp_id)
        same=True
        for addr in sorted(set(list(wd.keys())+list(self.keys()))):
            v0=self.get(addr, 0)
            v1=wd.get(addr, 0)
            same|=(v0==v1)
            if v0!=v1 and verbose:
                print("%20s, @0x%08x: file: 0x%08x, fpga: 0x%08x"%( region_name(addr), addr, v0, v1))
        return same

class ParseError(Exception):
    pass

if __name__=="__main__":
    wd=WordDict()
    wd.read(1)
    wd.dump()
