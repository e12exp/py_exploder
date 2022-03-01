#!/usr/bin/python3

from mainParser import parse, load
import socket
import sys

if __name__=="__main__":
    hostname=socket.gethostname()
    settings, mappings=load()
    if len(sys.argv)<2:
        print("Usage: %s {load|verify|scaler}")
    if sys.argv[1]=="load":
        print("loading %s settings into exploders"%hostname)
        for k,v in mappings[hostname].items():
            print("%s -> %s"%(k,v))
            settings[v].write(k)
            settings[v].verify(k)
    elif sys.argv[1]=="verify":
        for k,v in mappings[hostname].items():
            settings[v].verify(k)
    elif sys.argv[1]=="scaler":
        print("scaler values:")
        for k,v in mappings[hostname].items():
            print ("=== %s (%s)==="%(k,v))
            settings[v].dump_scalers(k, latched=True)
    else:
        print("unknown command: %s"%sys.argv[1])
        exit(1)

