"""Parse an object connecting an internal line (dt%d, bp%d) to inputs and outputs"""

from word_dict import *
import mainParser

def parse(d, wd):
    """parse a litaral assignment, set addr val"""
    if type(d)!=type("") or not d.startswith("require"):
        raise ParseError
    mainParser.parse(mainParser.settings_in[d.split(" ")[1]])
    
if __name__=="__main__":
    print(parseInput("tbus1.3"))
    print(parseInternal("bp12"))
    print(parseOutput("mbs12"))
