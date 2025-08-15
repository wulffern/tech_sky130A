#!/usr/bin/env python3

import re
import os
import glob

exclude = {
    "JNW_TR_SKY130A" : False,
    "JNW_ATR_SKY130A" : False,
    }

class MagUse:

    def __init__(self,parent,line):

        self.line = line
        self.parent = parent
        self.library = ""
        arr = re.split(r"\s+",line)
        self.cellname = arr[1]
        self.instanceName = arr[2]

        if(len(arr) > 3):
            self.library = arr[3]

    def __str__(self):
        return "use " + self.cellname + " " + self.instanceName + " " + self.library + "\n"


    def getAndFixPath(self):
        #- Find the magic files from cellname

        log = logging.getLogger()

        #- First check the parent directory
        #filepath = self.parent.dirname + os.path.sep + self.cellname  + ".mag"
        #if(os.path.exists(filepath)):
        #    self.library = ""
        #    return filepath

        filepath = None

        #- Check ../*/cellname.mag
        path = self.parent.dirname + os.path.sep + ".." + os.path.sep + "**" + os.path.sep+ self.cellname  + ".mag"
        files = glob.glob(path)
        if(len(files) == 1):
            filepath = files[0]
            dirn = os.path.basename(os.path.dirname(filepath))
            filepath = "../" + dirn + "/" + self.cellname + ".mag"
            self.library = "../" + dirn

        elif(len(files) > 1):
            log.error("Multiple paths with same filename")
            return None

        #if(filepath is None):
        #    log.info(f"Could not find path {self.cellname}")


        return filepath



class MagFile:

    def __init__(self,filename):
        self.filename = filename
        self.buffer = list()
        if(os.path.sep not in filename):
            self.dirname = "."
        else:
            self.dirname = os.path.dirname(filename)

        self.library = os.path.basename(self.dirname)
        self.basename = os.path.basename(filename)
        self.use = dict()
        self.children = dict()

        self.read()

    def read(self):
        self.buffer = list()
        self.hasUse = False
        log = logging.getLogger()
        #log.info(f"Reading {self.filename}")
        with open(self.filename) as fi:
            for line in fi:
                self.buffer.append(line)

                if(re.search(r"^\s*use",line)):
                    self.hasUse = True
                    self.use[line] = MagUse(self,line)
                    path = self.use[line].getAndFixPath()
                    if(path not in self.children and path is not None):
                        self.children[path] = MagFile(path)


    def write(self):

        if(self.library in exclude):
            return

        if(not self.hasUse):
            return

        #print("")

        #print(self.filename)
        ss = ""
        for line in self.buffer:
            if(line in self.use):
                ss += str(self.use[line])
                nline = str(self.use[line])
                oline = self.use[line].line
                if(oline != line):
                    print("New: ",nline,end="")
                    print("Old: ",oline,end="")
            else:
                ss += line

        log = logging.getLogger()

        log.info(f"Writing {self.filename}")
        with open(self.filename,"w") as fo:
            fo.write(ss)

        for m in self.children.values():
            m.write()

import click
import logging

@click.command()
@click.argument("filename")
def cli(filename):

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()

    if(not os.path.exists(filename)):
        log.error(f"Could not find {filename}")
        return

    dirn = os.path.dirname(filename)
    os.chdir(dirn)
    fname = os.path.basename(filename)

    m = MagFile(fname)

    m.write()



if __name__ == "__main__":

    cli()
