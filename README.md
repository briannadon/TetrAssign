# TetrAssign

## Introduction
### What does TetrAssign do?
TetrAssign is a python-based package that attempts to reconstruct the subgenomes of ancient paleotetraploid genomes.
It uses a single known paleotetraploid genome and a single close relative lacking that paleotetetraploidy to try to build a parsimonious reconstruction of what the tetraploid subgenomes looked like immediately after the duplication event using the non-duplicated relative as a reference. It only needs two FASTA files (the genes/CDSs/Proteins to be aligned) and two GFF/BED files (the genes' coordinates in the genomes). TetrAssign reconstructs using the assumption that the fewest number of inter- and intra-chromosomal rearrangements (fusions, fissions, translocations, inversions, etc) have occurred. 
### What doesn't it do?
This software cannot align more than 2 genomes at a time. It does not offer any kind of likelihood statistics for the putative chromosome-scale reconstructions it outputs. It cannot handle paleohexaploidies, octaploidies, or anything more than a tetraploidy (duplication). The assumptions underlying the method used by TetrAssign cannot currently be modified. 

## Installation
### Requirements
* UNIX, Linux, or Mac OS machine
... Windows is not supported currently.
* Python 2.7
* NCBI Command-line blast+ version 2.2.18 (other versions untested): ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.18/
* MCScanX (http://chibba.pgml.uga.edu/mcscan2/)
... Also, ensure MCScanX is included in your PATH, for example: `export PATH=$PATH:/path/to/MCScanX`
### Installing
After obtaining the required dependencies (see "Requirements" above), use:
```
git clone https://github.com/briannadon/TetrAssign.git
```
Ensure MCScanX is in your PATH (see above).
## Running

For a full list of the command-line options that TetrAssign uses, use `./Tetrassign.py -h` or `./TetraAssign.py --help`.

### Inputs
Tetrassign needs four files as inputs: A FASTA file containing all the genes in the genome (CDS or mRNA, Protein support coming soon), and a BED file containing coordinates for those genes for both the reference and putative paleotetraploid genomes. Before running the program, it is highly recommended that you **make sure the gene names match EXACTLY between the BED and FASTA files. This is the source of most errors.** Furthermore, you should ensure the BED files use unique names for the chromosomes of each species. For instance, if you are using maize and sorghum, you would want to name maize's chromosomes e.g. "Zm01, Zm02" and not "Chr01, Chr02".

### Command
Running `TetrAssign.py -h` will print:
```
usage: TetrAssign.py [-h] [-tf TETFASTAFILE] [-rf REFFASTAFILE]
                     [-rb REFBEDFILE] [-tb TETBEDFILE]
```
The `-rf` and `-tf` options specify the reference (diploid) FASTA and tetraploid FASTA files respectively, with `-rb` and `-tb` specifying the reference and tetraploid BED coordinate files.  These are required. Running the following will use the example data to build subgenomes for maize (paleotetraploid) against sorghum (diploid reference) chromosomes:
```
./Tetrassign.py -tf exampledata/Zm.cds.fa -rf exampledata/Sb.cds.fa -tb exampledata/Zm.bed -rb exampledata/Sb.bed
```
After some time running, 10 files will be produced with the names of the sorghum chromosomes ("Sb01" etc) and the subgenomes ("Sb01.subs.txt").

### Outputs
A set of text files describing the imputed ancient subgenomes for the tetraploid species. Each is a tab-separated file with the first column showing the genes of the reference chromosome, in order, and two columns to the right of that, each representing one imputed subgenome.  The assignment of which subgenome goes to which of the 2 right columns is arbitrary.
