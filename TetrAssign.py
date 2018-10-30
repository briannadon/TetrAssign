from sys import argv
from glob import glob
import re
import blockparse
import argparse
import subprocess


def blastn(tetfastafile,reffastafile,threads=2):
    makedbcmd = ("makeblastdb -dbtype nucl -in " + reffastafile
            + "-out tmpdb")
    makedbcmd = makedbcmd.split()
    subprocess.check_call(makedbcmd)

    blastncmd = ("blastn -db tmpdb -query " +tetfastafile+"  -max_target_seqs 2 -outfmt 6"
            "-out blastout.txt -evalue 1e-10 -num_threads "+threads)
    blastncmd = blastncmd.split()
    subprocess.check_call(blastncmd)

def reformatbed(bedfile):
    w = open('tmp.bed','w')
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
            newname1 = genenamedict[line[0]]
            newname2 = genenamedict[line[1]]
            line[0] = newname1
            line[1] = newname2
            line = '\t'.join(line)
            newblast.write(line + '\n')

def mcscan(blastfile='tmp.blast',bedfile='tmp.bed'):
    mccmd = "MCScanX ./tmp"
    subprocess.check_call(mccmd)

def getPrefix(bedfile):
    with open(bedfile) as b:
        fline = f.readline()
        fline = fline.strip().split('\t')
        rem = re.match('\w\w(?=\d\d)',line[0])
        prefix = rem.group()
        return(prefix)

def catfiles(file1,file2):
    filenames = [file1,file2]
    with open('tmp.bed', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

if __name__ == "__main__":
    parser= argparse.ArgumentParser(description = "Placeholder")
    parser.add_argument("-o", "--output", help="(optional) name the output file",dest='outfile')
    parser.add_argument("-tf", "--tetraploid-fasta", action="store",dest='tetfastafile')
    parser.add_argument("-rf", "--reference-fasta",dest='reffastafile')
    parser.add_argument("-rb",action="store",dest='refbedfile')
    parser.add_argument("-tb",action="store",dest='tetbedfile')

    options = parser.parse_args()
    if not (options.tetfastafile or options.tetbedfile or options.reffastafile):
        parser.error("Missing one of the required tetraploid or reference FASTA or bed files!")
    
    refprefix = get_prefix(options.refbedfile)
    tetprefix= get_prefix(options.tetbedfile)

    catfiles(options.refbedfile,options.tetbedfile)

    blastn(options.tetfastafile,options.reffastafile,threads=2)
    newnamedict = reformatbed(options.bedfile)
    reformatblast('blastout.txt',newnamedict)
    mcscan('tmp.blast','tmp.bed')
    blockparse.blockparse('tmp.collinearity',refbedfile,refprefix,tetprefix)
