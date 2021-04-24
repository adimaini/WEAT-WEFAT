#!/bin/sh
#SBATCH --time 1:00:00
#SBATCH -o testing%j.out
#SBATCH -e testing%j.err
#SBATCH -p short
#SBATCH --mail-user=adimaini@gwu.edu 
#SBATCH --mail-type=ALL

module load python3/3.7.2
source "/lustre/groups/caliskangrp/adimaini/twitter-corpus/twitter-env/bin/activate"
cd /lustre/groups/caliskangrp/adimaini/twitter-corpus

python3 tweets_to_embeddings.py