# TetrAssign

## Introduction
### What does TetrAssign do?
TetrAssign is a python-based package that attempts to reconstruct the subgenomes of ancient paleotetraploid genomes.
It uses a single known paleotetraploid genome and a single close relative lacking that paleotetetraploidy to try to build a parsimonious reconstruction of what the tetraploid subgenomes looked like immediately after the duplication event using the non-duplicated relative as a reference. It only needs two FASTA files (the genes/CDSs/Proteins to be aligned) and two GFF/BED files (the genes' coordinates in the genomes).  
### What doesn't it do?
This software cannot align more than 2 genomes at a time. It does not offer any kind of likelihood statistics for the putative chromosome-scale reconstructions it outputs. It cannot handle paleohexaploidies, octaploidies, or anything more than a tetraploidy (duplication).

## Installation
### Requirements
* UNIX, Linux, or Mac OS machine
...Windows is not supported currently.
* Python 2.7
* NCBI Command-line blast+ version 2.2.18 (other versions untested): ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.18/
* MCScanX (http://chibba.pgml.uga.edu/mcscan2/)
...Also, ensure MCScanX is included in your PATH: `export PATH=$PATH:/path/to/MCScanX`
### Installing
After obtaining the required dependencies (see "Requirements" above), use:
```git clone https://github.com/briannadon/TetrAssign.git``` 
Ensure MCScanX is in your PATH (see above).
## Running
 
