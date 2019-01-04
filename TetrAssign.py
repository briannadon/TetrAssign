#!/usr/bin/python
from sys import argv
from glob import glob
import re
import blockparse
import argparse
import subprocess


def blastn(tetfastafile,reffastafile,threads=2):
    makedbcmd = ("makeblastdb -dbtype nucl -in " + reffastafile)
    makedbcmd = makedbcmd.split()
    subprocess.check_call(makedbcmd)

    blastncmd = ("blastn -db "+reffastafile+" -query " +tetfastafile
            +"  -max_target_seqs 2 -outfmt 6"
            " -out blastout.txt -evalue 1e-10 -num_threads "+str(threads))
    blastncmd = blastncmd.split()
    subprocess.check_call(blastncmd)

def reformatbed(bedfile):
    w = open('tmp.gff','w')
    genenamedict = {}
    with open(bedfile) as b:
        for line in b:
            line = line.strip().split('\t')
            newname = '.'.join([line[0],line[1]])
            genenamedict[line[1]] = newname
            newline = '\t'.join([line[0],newname,line[2],line[3]])
            w.write(newline + '\n')
        w.close()
    return genenamedict

def reformatblast(blastfile,genenamedict):
    newblast = open('tmp.blast','w')
    with open(blastfile) as b:
        for line in b:
            line = line.strip().split('\t')
            if line[0] in genenamedict and line[1] in genenamedict:
                newname1 = genenamedict[line[0]]
                newname2 = genenamedict[line[1]]
                line[0] = newname1
                line[1] = newname2
                line = '\t'.join(line)
                newblast.write(line + '\n')

def mcscan():
    mccmd = "MCScanX ./tmp"
    mccmd = mccmd.split()
    subprocess.check_call(mccmd)

def getPrefix(bedfile):
    with open(bedfile) as f:
        fline = f.readline()
        fline = fline.strip().split('\t')
        rem = re.match('\w\w(?=\d\d)',fline[0])
        prefix = rem.group()
        return(prefix)

def catfiles(file1,file2,out):
    filenames = [file1,file2]
    with open(out, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

if __name__ == "__main__":
    parser= argparse.ArgumentParser(description = 
            """TetrAssign: a lightweight tool to parsimoniously reconstruct diploid 
            ancestral genome states in paleotetraploid genomes. 
            Requires NCBI Blast 2.2.18 and MCScanX. 
            Ensure you have appropriately formatted BED and Protein/CDS FASTA files 
            for both your paleotetraploid and diploid species before starting.
            """
            )
    parser.add_argument("-tf", "--tetraploid-fasta", action="store",dest='tetfastafile')
    parser.add_argument("-rf", "--reference-fasta",dest='reffastafile')
    parser.add_argument("-rb",action="store",dest='refbedfile')
    parser.add_argument("-tb",action="store",dest='tetbedfile')

    options = parser.parse_args()
    if not (options.tetfastafile or options.tetbedfile or options.reffastafile or options.refbedfile):
        parser.error("Missing one of the required tetraploid or reference FASTA or bed files!")
    
    refprefix = getPrefix(options.refbedfile)
    tetprefix= getPrefix(options.tetbedfile)

    catfiles(options.refbedfile,options.tetbedfile,'combined.bed')

    blastn(options.tetfastafile,options.reffastafile,threads=2)
    newnamedict = reformatbed('combined.bed')
    reformatblast('blastout.txt',newnamedict)
    mcscan()
    blockparse.blockparse('tmp.collinearity','tmp.gff',refprefix,tetprefix)
