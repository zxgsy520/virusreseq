# virusreseq
Viral genome mutation analysis

## System requirements
They have been developed and tested using the following packages/tools:
+ [miniconda3](https://conda.io/en/latest/miniconda.html) (Python 3.8)
+ [lofreq](https://github.com/CSB5/lofreq) (version 2.1.5)
+ [gatk](https://github.com/broadinstitute/gatk) (version 4.2.3.0)
+ [mpileup2readcounts](https://github.com/gatoravi/mpileup2readcounts) (version 1.0.0)
+ [samtools](https://github.com/samtools/samtools) (version 1.12-15)
+ [bwa](https://github.com/lh3/bwa) (version 0.7.17)
+ [snippy](https://github.com/tseemann/snippy) (version 4.5.9)

## Usage
### Obtain the mutation information of a locus
```
samtools mpileup -aa -f genome.fasta rmdup.bam |mpileup2readcounts |counts2mutation.py >mutation.xls
```
+ result：[mutation.xls](https://github.com/zxgsy520/virusreseq/blob/main/docs/mutation.xls)
