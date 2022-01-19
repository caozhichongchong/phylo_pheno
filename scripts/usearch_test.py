import glob
import os
test_otus = 'geno_pheno/database/85_otus.fasta.all.V4_v5.fasta'
ncbi_16s = 'geno_pheno/database/ncbi_16s.fasta'

makedb = 'usearch -makeudb_usearch %s -output %s.udb' % (ncbi_16s, ncbi_16s)

os.system(makedb)

script_folder = 'geno_pheno/scripts/'
try:
    os.mkdir(script_folder)
except IOError:
    pass

def usearch_blast(genome, database):
    cmds = '#!/bin/bash\nsource ~/.bashrc\n'
    cmds += 'usearch -ublast %s -db %s.udb -strand both -evalue 1e-2 -accel 0.5 -blast6out %s.usearch.b6 -threads 40' % (genome, database, genome)
    return cmds


all_genomes = glob.glob('geno_pheno/genomes/*.fasta')

i = 0
cmds = ''
for genome in all_genomes:
    cmds += usearch_blast(genome, ncbi_16s)
    i += 1
    if i % 2 == 0:
        f1 = open('%s/%s.usearch.sh' % (script_folder, i), 'w')
        f1.write(cmds)
        f1.close()
        cmds = ''

# generate a bash file to submit all jobs
allscripts = glob.glob('%s/*.usearch.sh' % (script_folder))

submitscript = '#!/bin/bash\nsource ~/.bashrc\n'
for script in allscripts:
    pref, script_suf = os.path.split(script)
    submitscript += 'jobmit %s %s small\n' % (script, script_suf)
f1 = open('%s/../submitalljob.sh' % (script_folder), 'w')
f1.write(submitscript)
f1.close()

