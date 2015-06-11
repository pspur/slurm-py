# bash script to sbatch all files ending in .sh in current dir:
# for f in *.sh; do sbatch "$f"; done

import os

# Grab first 30 chars of each merged .bam filename in target directory, 
# ie. 2142_CTGAAGCT_H0GFDALXX_merged, and store in list

fnameprefixes = []
for dirpath, dirs, files in os.walk("/gpfs/scratch/jw24/gatk/SIM_bams"):
  path = dirpath.split('/')
  for f in files:
    if f.endswith("merged_dedup.bam"):
      fnameprefixes.append(f[0:30])

# Write SLURM script for each member in fnameprefixes[]
# Flagstat is command being run

for prefix in fnameprefixes:
  with open("slurm_fstat_{0}.sh".format(prefix[0:22]),"w") as fout:
    fout.write('#!/bin/sh\n\n')
    fout.write('#SBATCH --partition=general-compute\n')
    fout.write('#SBATCH --time=01:00:00\n')
    fout.write('#SBATCH --nodes=1\n')
    fout.write('#SBATCH --mem=6000\n')
    fout.write('#SBATCH --ntasks-per-node=1\n')
    fout.write('#SBATCH --job-name=flagstat_bam_{0}\n'.format(prefix))
    fout.write('#SBATCH --output={0}_dedup_bam.log\n'.format(prefix))
    fout.write('#SBATCH --mail-user=paulspur@buffalo.edu\n')
    fout.write('#SBATCH --mail-type=END\n\n')
    fout.write('echo "SLURM_JOBID="$SLURM_JOBID\n')
    fout.write('echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST\n')
    fout.write('echo "SLURM_NNODES"=$SLURM_NNODES\n')
    fout.write('echo "SLURMTMPDIR="$SLURMTMPDIR\n')
    fout.write('echo "working directory = "$SLURM_SUBMIT_DIR\n\n')
    fout.write('ulimit -s unlimited\n')
    fout.write('module load samtools\n')
    fout.write('module list\n\n')
    fout.write('echo "Launch job"\n\n')
    fout.write('samtools flagstat /gpfs/scratch/jw24/gatk/')
    fout.write('SIM_bams/{0}/{1}_dedup.bam > '.format(prefix[0:4],prefix))
    fout.write('{0}_dedup_bam.fstat\n\n'.format(prefix))
    fout.write('echo "All Done!"')
