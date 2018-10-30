import re
from sys import argv
import csv

class Vividict(dict):
    def __missing__(self,key):
        value = self[key] = type(self)()
        return value

def reformatCollinearity(colfile,reformattedname='collinearity_reformat.txt'):
    w = open(reformattedname,'w')
    with open(colfile) as c:
        for line in c:
            if re.search('^#',line):
                next
            else:
                line = re.sub(' |:','',line)
                line = re.sub('-','\t',line,1)
                w.write(line)
    w.close()

def collinearityToDict(collinearityfile):
    cdict = Vividict()
    with open(collinearityfile) as c:
        for line in c:
            line = line.strip().split()
            cdict[int(line[0])][line[2]] = line[3]
    return cdict

def getRefChroms(gfffile,chrname='Sb'):
    refdict = {}
    with open(gfffile) as g:
        for line in g:
            if chrname in line:
                line = line.strip().split('\t')
                if line[0] in refdict:
                    refdict[line[0]].append(line[1])
                else:
                    refdict[line[0]] = [line[1]]
    return refdict

def addToSub(index,sublist,block):
    for ref,ortho in block.items():
        if not sublist[index][ref]:
            sublist[index][ref] = ortho

def addBlockByChr(blockdump,sublist,chrreg='Zm\d+'): #ought to only do it once
    for i,sub in enumerate(sublist):
        vals = sub.values()
        chrs = [re.search(chrreg,val).group() for val in vals if re.search(chrreg,val)]
        for chrom in chrs:
            for block in blockdump[:]:
                if any(chrom in bv for bv in block.values()) and block in blockdump:
                    addToSub(i,sublist,block)
                    blockdump.remove(block)

def dumpBlocks(collinearitydict,refchrom):
    blockdump = []
    for blockid, block in collinearitydict.items():
        brefgenes = block.keys()
        if any(g in refchrom for g in brefgenes) and block not in blockdump:
            blockdump.append(block)
    return blockdump

def assignSubgenomes(refchrom,collinearitydict,chrreg = 'Zm\d+'):
    sublist = [Vividict(),Vividict()]
    blockdump = dumpBlocks(collinearitydict,refchrom)
    for i,sub in enumerate(sublist):
        if not sub:
            for block in blockdump:
                btestchr = next(re.search(chrreg,btv).group() for btv in block.values() if re.search(chrreg,btv))
                if not any(btestchr in sk for sk in [s.keys() for s in sublist]):
                    sublist[i] = block
                    blockdump.remove(block)
                    addBlockByChr(blockdump,sublist,chrreg)
                    break
    for refgene in refchrom:
        for i,sub in enumerate(sublist):
            if refgene in sub.keys():
                continue
            else:
                for block in blockdump[:]:
                    if refgene in block.keys() and set(block.keys()).isdisjoint(sub.keys()):
                        addToSub(i,sublist,block)
                        blockdump.remove(block)
                        addBlockByChr(blockdump,sublist,chrreg)
    return sublist


def blockparse(collinearityfile,gfffile,refprefix='Sb',tetprefix='Zm'):
    refchroms = getRefChroms(gfffile,chrname=refprefix)
    reformatCollinearity(collinearityfile,reformattedname='tmpcol.txt')
    coldict = collinearityToDict('tmpcol.txt')
    for refchrom in sorted(refchroms.keys()):
        print(refchrom)
        sublist = assignSubgenomes(refchroms[refchrom],coldict,tetprefix+'\d+')
        w = open(refchrom + ".subs.txt",'w')
        for refgene in refchroms[refchrom]:
            if refgene in sublist[0]:
                sub1 = sublist[0][refgene]
            else:
                sub1 = ''
            if refgene in sublist[1]:
                sub2 = sublist[1][refgene]
            else:
                sub2 = ''
            line = refgene+'\t'+sub1+'\t'+sub2
            w.write(line + '\n')

