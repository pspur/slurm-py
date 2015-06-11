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
# gatk is command being run

for prefix in fnameprefixes:
  with open("gatk_slurm_{0}.sh".format(prefix[0:22]),"w") as fout:
    fout.write('#!/bin/sh\n\n')
    fout.write('#SBATCH --partition=general-compute\n')
    fout.write('#SBATCH --time=72:00:00\n')
    fout.write('#SBATCH --nodes=1\n')
    fout.write('#SBATCH --mem=12000\n')
    fout.write('#SBATCH --ntasks-per-node=1\n')
    fout.write('#SBATCH --job-name=gatk_bam_{0}\n'.format(prefix))
    fout.write('#SBATCH --output={0}_gatk_bam.log\n'.format(prefix))
    fout.write('#SBATCH --mail-user=paulspur@buffalo.edu\n')
    fout.write('#SBATCH --mail-type=END\n\n')
    fout.write('echo "SLURM_JOBID="$SLURM_JOBID\n')
    fout.write('echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST\n')
    fout.write('echo "SLURM_NNODES"=$SLURM_NNODES\n')
    fout.write('echo "SLURMTMPDIR="$SLURMTMPDIR\n')
    fout.write('echo "working directory = "$SLURM_SUBMIT_DIR\n\n')
    fout.write('ulimit -s unlimited\n')
    fout.write('module load java/1.8.0_45\n')
    fout.write('module load gatk\n')
    fout.write('module list\n\n')
    fout.write('echo "Launch job"\n\n')
    fout.write('java -Xmx10g -jar $GATK_HOME/GenomeAnalysisTK.jar -T ')
    fout.write('DepthOfCoverage -R /gpfs/util/ccr/data/Broad/gatk_bundle/2.8')
    fout.write('/human_g1k_v37_decoy.fasta ')
    fout.write('-o {0}.out '.format(prefix)) 
    fout.write('-I /gpfs/scratch/jw24/gatk/SIM_bams/')
    fout.write('{0}/{1}_dedup.bam\n\n'.format(prefix[0:4],prefix))
    fout.write('echo "All Done!"')
