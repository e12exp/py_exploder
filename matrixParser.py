"""Parse an object connecting an internal line (dt%d, bp%d) to inputs and outputs"""

from word_dict import *

internalList=[
    ("dt(\d+)", lambda n:  0+inRange(n, 0, 15)),
    ("bp(\d+)", lambda n: 16+inRange(n, 0, 15)),
    # note: the other outputs of the input matrix are not supported for now.
    # (they are: global dt, veto, gate generator flipflops)
]

inputList=[
    ("tbus([01])[.]([0-7])", lambda n,m: 8*n+m),
    ("lemo([0-7])",          lambda n:   16+n),
    ("pulser([0-3])",        lambda n:   24+n),
    ("mbs_tdt",              lambda:     28),
    ("mbs_ms",               lambda:     29),
    # 30..31: reserved
    ("sfp(\d+)[.](\d+)",   lambda n,m: 32+16*inRange(n, 0, 4)+inRange(m, 0, 15))
    # flip-flops: not implemented
]
outputList=[
    ("mbs(\d+)",           lambda n: 0+inRange(n, 1, 15)),
    # mbs N actually sets the lines N[3:0]?!
    ("tbusX[.]?([0-7])",   lambda n:16+n),
    ("lemo([0-7])",        lambda n:24+n),
    ("lvds([0-7])",        lambda n:32+n),
    ("scaler([0-7])",      lambda n:40+n),
    ("scaler_rst([0-7])",  lambda n:48+n),
    ("scaler_gate([0-7])", lambda n:56+n),
    ("sfp(\d+)[.](\d+)",   lambda n,m: 64+16*inRange(n, 0, 3)+inRange(m, 0, 15))
]

def parseIO(name, l):
    for regex, f in l:
        m=re.match(regex, name)
        if m:
            try:
                return f(*map(int, m.groups()))
            except ValueError as e:
                raise Exception("Could not parse '%s'"%name) from e
    raise Exception("Could not parse name %s."%name)

parseInput=   lambda n:parseIO(n, inputList)
parseInternal=lambda n:parseIO(n, internalList)
parseOutput=  lambda n:parseIO(n, outputList)

def parse(d, wd):
    """parse an internal line statement, connecting [inputs]->internal->[outputs]"""
    try:
        intId=parseInternal(d["name"])
    except Exception as e:
        raise ParseError from e
    if d["name"] in wd.lines:
        print("Internal line %s is used in multiple statements. Overall assignment will be ORed."%d["name"])
    wd.lines.append(d["name"])
    inIds=lmap(parseInput, d.get("in", []))
    outIds=lmap(parseOutput, d.get("out", []))
    for i in filter(lambda i:0<=i and i<8, map(lambda i:i-40, outIds)):
        if "label" not in d:
            raise Exception("Scaler %d assignment (using %s) is missing label."%(i, d["name"]))
        if i in wd.labels:
            raise Exception("Warning: scaler %d is assigned to multiple lines"%i)
            wd.labels[i]+="|"+d["label"]
        else:
            wd.labels[i]=d["label"]
            
    #print(intId, inIds, outIds)

    # first, input matrix.
    # as we cut corners on parsing intId, the intId (n in documentation) will always come out less than 32.
    for i in inIds:
        if i < 32: 
            wd.setBit(0x00+intId, i)
        else:
            i0=i//32
            i1=i%32
            wd.setBit(0x1000+i0+4*intId, i1)
            # set address 0x0+intId, bit i.
    # output matrix
    for o in outIds:
        if o < 64:
            wd.setBit(0x40+o, intId)
        else:
            wd.setBit(0x1200+4*o, intId)

if __name__=="__main__":
    print(parseInput("tbus1.3"))
    print(parseInternal("bp12"))
    print(parseOutput("mbs12"))
