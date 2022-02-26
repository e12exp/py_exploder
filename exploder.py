#!/usr/bin/python3

from mainParser import parse, load

if __name__=="__main__":
    settings, mappings=load()
    #    mp.parse({"name":"bp0", "in":["lemo0", "lemo2"], "out":["mbs12", "lemo3"]},  wd)
    for name, wd in settings.items():
        print("==%s=="%name)
        #wd.dump()
    settings["master"].write(0)
    settings["master"].verify(0)

