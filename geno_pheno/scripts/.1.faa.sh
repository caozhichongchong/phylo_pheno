#!/bin/bash
source ~/.bashrc
diamond blastp --query geno_pheno/genomes/1.faa --db geno_pheno/database/Butyrate.pro.fasta.dmnd --out geno_pheno/genomes/1.faa.diamond.txt --outfmt 6 --max-target-seqs 2 --evalue 1e-2 --threads 4
